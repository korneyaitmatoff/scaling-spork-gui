from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class IncomingRequestForm(FlaskForm):
    dean_name = StringField('ФИО декана факультета/директора института:', validators=[DataRequired()])
    student_name = StringField('ФИО студента:', validators=[DataRequired()])
    education_form = SelectField('Форма обучения:',
                               choices=[('', 'Выберите форму обучения'),
                                        ('очная', 'Очная'),
                                        ('заочная', 'Заочная'),
                                        ('очно-заочная', 'Очно-заочная')],
                               validators=[DataRequired()])
    education_basis = SelectField('Основа обучения:',
                                choices=[('', 'Выберите основу обучения'),
                                         ('бюджетная', 'Бюджетная'),
                                         ('коммерческая', 'Коммерческая')],
                                validators=[DataRequired()])
    faculty = StringField('Факультет/институт:', validators=[DataRequired()])
    course = StringField('Курс:', validators=[DataRequired()])
    group = StringField('Группа:', validators=[DataRequired()])
    phone = StringField('Контактный телефон:', validators=[DataRequired()])
    reason = TextAreaField('Причина нуждаемости в материальной помощи:', validators=[DataRequired()])
    submit = SubmitField('Сформировать заявление')