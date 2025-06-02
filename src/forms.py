from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

class SearchStudentForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=100)])
    submit = SubmitField('Search')

class AddStudentForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    group_code = StringField('Group Code', validators=[
        DataRequired(message='Group code is required'),
        Length(min=2, max=20, message='Group code must be between 2 and 20 characters')
    ])
    inn = StringField('INN', validators=[
        DataRequired(message='INN is required'),
        Length(min=10, max=12, message='INN must be 10-12 digits'),
        Regexp(r'^\d+$', message='INN must contain only digits')
    ])
    serial_number = StringField('Passport Serial Number', validators=[
        DataRequired(message='Serial number is required'),
        Length(min=6, max=20, message='Serial number must be between 6 and 20 characters')
    ])
    birthdate = DateField('Birth Date', validators=[
        DataRequired(message='Birth date is required')
    ])
    is_resident = BooleanField('RF Resident', default=True)
    submit = SubmitField('Add Student')

class IncomingRequestForm(FlaskForm):
    dean_name = StringField('ФИО декана факультета/директора института', validators=[
        DataRequired(message='Dean name is required'),
        Length(min=2, max=100, message='Dean name must be between 2 and 100 characters')
    ])
    student_name = StringField('ФИО студента', validators=[
        DataRequired(message='Student name is required'),
        Length(min=2, max=100, message='Student name must be between 2 and 100 characters')
    ])
    education_form = SelectField('Форма обучения', choices=[
        ('full-time', 'Очная'),
        ('part-time', 'Заочная')
    ], validators=[DataRequired(message='Education form is required')])
    education_basis = SelectField('Основа обучения', choices=[
        ('budget', 'Бюджет'),
        ('contract', 'Коммерция'),
    ], validators=[DataRequired(message='Education basis is required')])
    faculty = StringField('Факультет/институт', validators=[
        DataRequired(message='Faculty is required'),
        Length(min=2, max=100, message='Faculty must be between 2 and 100 characters')
    ])
    course = IntegerField('Курс', validators=[
        DataRequired(message='Course is required'),
        NumberRange(min=1, max=6, message='Course must be between 1 and 6')
    ])
    group = StringField('Группа', validators=[
        DataRequired(message='Group is required'),
        Length(min=2, max=20, message='Group must be between 2 and 20 characters')
    ])
    phone = StringField('Контактный телефон', validators=[
        DataRequired(message='Phone is required'),
        Length(min=10, max=20, message='Phone must be between 10 and 20 characters'),
        Regexp(r'^[\d\+\-\(\)\s]+$', message='Phone must contain only digits, +, -, (, ), and spaces')
    ])
    reason = TextAreaField('Причина нуждаемости в материальной помощи', validators=[
        DataRequired(message='Reason is required'),
        Length(min=10, max=1000, message='Reason must be between 10 and 1000 characters')
    ])
    submit = SubmitField('Сформировать заявление')
