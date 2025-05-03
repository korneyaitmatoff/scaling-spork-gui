from app import app

from flask import (
    render_template,
    session,
    redirect,
)
from src.dependencies import api
from src.forms import LoginForm


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

    if form.is_submitted():
        response = api.is_employee_creds_correct(login=form.login.data, password=form.password.data)

        if response is True:
            session["is_auth"] = response

            return redirect(location="/index")
        else:
            ...
        # TODO: realize errors output

    return render_template('index.html', title="Login", form=form)


# TODO: make page for students
# TODO: make page for employees
# TODO: make page for votes
# # TODO: make page for make vote
# TODO: make page for protocol
# TODO: decorate main page