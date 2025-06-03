from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField, \
    TimeField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Optional


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
    dean_name = StringField('Dean Name', validators=[
        DataRequired(message='Dean name is required'),
        Length(min=2, max=100, message='Dean name must be between 2 and 100 characters')
    ])
    student_name = StringField('Student Name', validators=[
        DataRequired(message='Student name is required'),
        Length(min=2, max=100, message='Student name must be between 2 and 100 characters')
    ])
    education_form = SelectField('Education Form', choices=[
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('evening', 'Evening'),
        ('distance', 'Distance')
    ], validators=[DataRequired(message='Education form is required')])
    education_basis = SelectField('Education Basis', choices=[
        ('budget', 'Budget'),
        ('contract', 'Contract'),
        ('target', 'Target')
    ], validators=[DataRequired(message='Education basis is required')])
    faculty = StringField('Faculty', validators=[
        DataRequired(message='Faculty is required'),
        Length(min=2, max=100, message='Faculty must be between 2 and 100 characters')
    ])
    course = IntegerField('Course', validators=[
        DataRequired(message='Course is required'),
        NumberRange(min=1, max=6, message='Course must be between 1 and 6')
    ])
    group = StringField('Group', validators=[
        DataRequired(message='Group is required'),
        Length(min=2, max=20, message='Group must be between 2 and 20 characters')
    ])
    phone = StringField('Phone', validators=[
        DataRequired(message='Phone is required'),
        Length(min=10, max=20, message='Phone must be between 10 and 20 characters'),
        Regexp(r'^[\d\+\-\(\)\s]+$', message='Phone must contain only digits, +, -, (, ), and spaces')
    ])
    reason = TextAreaField('Reason for Financial Aid', validators=[
        DataRequired(message='Reason is required'),
        Length(min=10, max=1000, message='Reason must be between 10 and 1000 characters')
    ])
    submit = SubmitField('Submit Application')


class VoteForm(FlaskForm):
    students = SelectField('Студент', choices=[], validators=[DataRequired()])
    submit = SubmitField('Проголосовать')
