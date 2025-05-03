from app import app

from flask import (
    render_template,
    session,
    redirect
)

from src.forms import LoginForm


# TODO: make decorator for check auth


@app.route("/")
@app.route("/index")
def index():
    if session.get("is_auth") is True:
        render_template('main_page.html', title="Main")

    return redirect(location="/login")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.is_submitted():
        print(form.login.data)

    return render_template('index.html', title="Login", form=form)
