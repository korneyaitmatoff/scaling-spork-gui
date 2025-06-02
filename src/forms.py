from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class SearchStudentForm(FlaskForm):
    name = StringField('Имя', validators=[Length(max=100)])
    submit = SubmitField('Поиск')

class AddStudentForm(FlaskForm):
    name = StringField('ФИО', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    group_code = StringField('Номер группы', validators=[
        DataRequired(message='Group code is required'),
        Length(min=2, max=20, message='Group code must be between 2 and 20 characters')
    ])
    inn = StringField('ИНН', validators=[
        DataRequired(message='INN is required'),
        Length(min=10, max=12, message='INN must be 10-12 digits'),
        Regexp(r'^\d+$', message='INN must contain only digits')
    ])
    serial_number = StringField('Серия и номер паспорта', validators=[
        DataRequired(message='Serial number is required'),
        Length(min=6, max=20, message='Serial number must be between 6 and 20 characters')
    ])
    birthdate = DateField('Дата рождения', validators=[
        DataRequired(message='Birth date is required')
    ])
    is_resident = BooleanField('Резидент РФ', default=True)
    submit = SubmitField('Добавить студента')
