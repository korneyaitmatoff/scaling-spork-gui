from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchStudent(FlaskForm):
    name = StringField(label="ФИО", validators=[DataRequired()])
    submit = SubmitField()
