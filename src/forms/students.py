from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class StudentsChoose(FlaskForm):
    id = StringField("ID")
    name = StringField("Name")
    group_code = StringField("Group code")
    submit = SubmitField("Просмотреть")
