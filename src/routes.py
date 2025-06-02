from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from src.models import User, get_db
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'


def login_required(f):
    """Decorator to require login for protected routes"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if 'user_id' in session:
        return redirect(url_for('students'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')

        # Get database session
        db = next(get_db())

        try:
            # Find user by username or email
            user = db.query(User).filter(
                (User.username == username) | (User.email == username)
            ).first()

            if user and user.is_active and check_password_hash(user.password_hash, password):
                # Login successful
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Welcome back, {user.username}!', 'success')

                # Redirect to next page if specified, otherwise dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('students'))
            else:
                flash('Invalid username or password', 'error')

        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
            print(f"Login error: {e}")
        finally:
            db.close()

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout handler"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('login'))



@app.route("/students")
def students():
    pass

@app.route("/votes")
def votes():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5003)
