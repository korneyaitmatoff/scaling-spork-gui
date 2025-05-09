from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddStudent(FlaskForm):
    name = StringField(label="ФИО", validators=[DataRequired()])
    group_code = StringField(label="Номер группы", validators=[DataRequired()])
    inn = StringField(label="ИНН")
    passport_data = StringField(label="Паспортные данные")
    is_resident = BooleanField(label="Гражданин РФ")
    submit = SubmitField(label="Создать")