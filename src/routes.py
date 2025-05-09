from datetime import date, datetime

from app import app

from flask import (
    render_template,
    session,
    redirect,
    request
)
from wtforms import Field
from src.dependencies import api
from src.forms import (
    LoginForm,
    StudentsChoose, AddStudent, SearchStudent
)
from src.forms.incoming_request import IncomingRequestForm


# TODO: make decorator for check auth


@app.route("/")
@app.route("/index")
def index():
    if session.get("is_auth") is True:
        return render_template('main_page.html', title="Main")

    return redirect(location="/login")


@app.route("/login", methods=["POST", "GET"])
def login():
    if session.get("is_auth") is True:
        return redirect(location="/index")

    form = LoginForm()
    message: str = None

    if form.is_submitted():
        response = api.is_employee_creds_correct(login=form.login.data, password=form.password.data)

        if response is True:
            session["is_auth"] = response

            return redirect(location="/index")
        else:
            message = "Неверный логин или пароль"

    return render_template('index.html', title="Login", form=form, message=message)


@app.route("/students", methods=["POST", "GET"])
def students():
    if session.get("is_auth") is not True:
        return redirect(location="/index")

    selected_id = request.args.get("selected_id", default=1, type=int)
    name = request.args.get("name", default="", type=str)

    search_student_form = SearchStudent()

    students_list: list[StudentsChoose] = []
    for item in api.get_students() if name == "" else api.get_students_by_name(name=name):
        form = StudentsChoose()
        form.id = item["id"]
        form.name = item["name"]
        form.group_code = item["group_code"]

        students_list.append(form)

    # prepare forms
    if (add_student_form := AddStudent()).is_submitted():
        print(
            {
                key: value.data for key, value in add_student_form.__dict__.items()
                if isinstance(value, Field) and key not in ("csrf_token", "submit")
            }
        )
        api.add_student(
            json={
                "name": add_student_form.name.data,
                "group_code": add_student_form.group_code.data,
                "inn": add_student_form.inn.data,
                "is_resident": add_student_form.is_resident.data,
                "passport_data": {
                    "serial_number": add_student_form.serial_number.data,
                    "birthdate": add_student_form.birthdate.data.strftime('%Y-%m-%d')
                }
            }
        )

    return render_template(
        template_name_or_list="students.html",
        title="Students",
        students=students_list,
        selected_student=api.get_student_by_id(s_id=selected_id)[0],
        add_student_form=add_student_form,
        search_form=search_student_form
    )


@app.route("/incoming_request", methods=["POST", "GET"])
def incoming_request():
    form = IncomingRequestForm()
    if form.is_submitted():
        form_data = {
            'dean_name': form.dean_name.data,
            'student_name': form.student_name.data,
            'education_form': form.education_form.data,
            'education_basis': form.education_basis.data,
            'faculty': form.faculty.data,
            'course': form.course.data,
            'group': form.group.data,
            'phone': form.phone.data,
            'reason': form.reason.data,
            'submission_date': datetime.now().strftime("%d.%m.%Y")
        }

        api.create_incoming_request(
            json={
                "reason": form.reason.data,
                "study_kind": form.education_basis.data,
                "student_name": form.student_name.data,
                "is_commerce": form.education_form.data in ("Коммерческая", "коммерческая"),
                "faculty": form.faculty.data,
                "course": form.course.data,
                "student_group_code": form.group.data,
                "contact": form.phone.data
            }
        )

        return render_template('incoming_request_result.html', data=form_data)

    return render_template('incoming_request.html', form=form)

# TODO: make page for employees
# TODO: make page for votes
# # TODO: make page for make vote
# TODO: make page for protocol
# TODO: decorate main page
