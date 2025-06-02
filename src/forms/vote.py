from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class VoteForm(FlaskForm):
    student = SelectField('Студент', choices=[], validators=[DataRequired()])
    submit = SubmitField('Проголосовать')
