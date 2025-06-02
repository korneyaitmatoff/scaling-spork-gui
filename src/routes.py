from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models import User, Student, get_db
from src.forms import SearchStudentForm, AddStudentForm
from functools import wraps
from sqlalchemy import or_

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
        return redirect(url_for('dashboard'))
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
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
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


@app.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard page"""
    username = session.get('username', 'User')
    return render_template('dashboard.html', username=username)


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == session['user_id']).first()
        return render_template('profile.html', user=user)
    finally:
        db.close()


@app.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    """Students page with search and add functionality"""
    db = next(get_db())

    try:
        search_form = SearchStudentForm()
        add_student_form = AddStudentForm()

        # Handle adding new student
        if request.method == 'POST' and add_student_form.validate_on_submit():
            try:
                # Check if INN already exists
                existing_student = db.query(Student).filter(Student.inn == add_student_form.inn.data).first()
                if existing_student:
                    flash('Student with this INN already exists', 'error')
                else:
                    new_student = Student(
                        name=add_student_form.name.data,
                        group_code=add_student_form.group_code.data,
                        inn=add_student_form.inn.data,
                        serial_number=add_student_form.serial_number.data,
                        birthdate=add_student_form.birthdate.data,
                        is_resident=add_student_form.is_resident.data
                    )
                    db.add(new_student)
                    db.commit()
                    flash(f'Student {new_student.name} added successfully!', 'success')
                    return redirect(url_for('students'))
            except Exception as e:
                db.rollback()
                flash('Error adding student. Please try again.', 'error')
                print(f"Error adding student: {e}")

        # Handle search
        students_query = db.query(Student)
        if search_form.name.data:
            search_term = f"%{search_form.name.data}%"
            students_query = students_query.filter(
                or_(
                    Student.name.ilike(search_term),
                    Student.group_code.ilike(search_term)
                )
            )

        students = students_query.order_by(Student.name).all()

        # Handle selected student
        selected_student = None
        selected_id = request.args.get('selected_id')
        if selected_id:
            try:
                selected_student = db.query(Student).filter(Student.id == int(selected_id)).first()
            except (ValueError, TypeError):
                pass

        return render_template('students.html',
                               students=students,
                               selected_student=selected_student,
                               search_form=search_form,
                               add_student_form=add_student_form)

    finally:
        db.close()


@app.route("/votes")
def votes():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5004)
