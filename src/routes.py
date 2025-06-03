from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models import User, Student, IncomingRequest, get_db, Vote
from forms import SearchStudentForm, AddStudentForm, IncomingRequestForm
from functools import wraps
from sqlalchemy import or_

from src.models import VoteEmployee, Protocol, VoteStudent

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
    """Home page - redirect to students if logged in, otherwise to login"""
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

                # Redirect to next page if specified, otherwise students
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


@app.route('/incoming_request', methods=['GET', 'POST'])
@login_required
def incoming_request():
    """Incoming request form page"""
    form = IncomingRequestForm()

    if form.validate_on_submit():
        db = next(get_db())
        try:
            new_request = IncomingRequest(
                dean_name=form.dean_name.data,
                student_name=form.student_name.data,
                education_form=form.education_form.data,
                education_basis=form.education_basis.data,
                faculty=form.faculty.data,
                course=form.course.data,
                group=form.group.data,
                phone=form.phone.data,
                reason=form.reason.data
            )
            db.add(new_request)
            db.commit()

            flash('Application submitted successfully!', 'success')
            return redirect(url_for('incoming_request_result', request_id=new_request.id))

        except Exception as e:
            db.rollback()
            flash('Error submitting application. Please try again.', 'error')
            print(f"Error submitting request: {e}")
        finally:
            db.close()

    return render_template('incoming_request.html', form=form)


@app.route('/incoming_request_result/<int:request_id>')
@login_required
def incoming_request_result(request_id):
    """Display the submitted request result"""
    db = next(get_db())
    try:
        request_data = db.query(IncomingRequest).filter(IncomingRequest.id == request_id).first()
        if not request_data:
            flash('Request not found', 'error')
            return redirect(url_for('students'))

        return render_template('incoming_request_result.html', request=request_data)
    finally:
        db.close()


@app.route('/votes', methods=['GET', 'POST'])
def votes(voting_id=None):
    from src.forms import VoteForm

    form = VoteForm()
    db = next(get_db())

    if form.is_submitted():
        # add user to VoteEmployee
        db.add(VoteEmployee(
            employee_id=session["user_id"],
            vote_id=request.args.get('voting_id'),
            protocol_id=db.query(Protocol).first().id
        ))
        # add student to VoteStudent
        db.add(VoteStudent(
            vote_id=request.args.get('voting_id'),
            student_id=form.students.data,
            protocol_id=db.query(Protocol).first().id
        ))
        db.commit()

        flash('Vote submitted successfully!', 'success')

    return render_template(
        'votes.html',
        form=form,
        students=[item for item in db.query(IncomingRequest).all()],
        votes=[item for item in db.query(Vote).all()]
    )


@app.route('/protocol', methods=['GET'])
def protocol():
    db = next(get_db())

    students = db.query(IncomingRequest).all()
    print([item for item in students])

    return render_template(
        "protocol.html",
        students=[item for item in students]
    )


if __name__ == '__main__':
    app.run(debug=True, port=5005)
