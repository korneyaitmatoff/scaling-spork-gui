from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchStudent(FlaskForm):
    name = StringField(label="Введите имя", validators=[DataRequired()])
    submit = SubmitField()