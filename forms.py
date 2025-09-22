from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class AutoForm(FlaskForm):
    """
    Форма авторизации пользователя в системе.
    Поля:
        email (StringField): Поле для ввода email с валидацией
        passwrd (PasswordField): Поле для ввода пароля
        submit (SubmitField): Кнопка отправки формы
    """
    email = StringField('Email:', validators=[DataRequired(), Email()])
    passwrd = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegForm(FlaskForm):
    """
    Форма регистрации нового пользователя.
    Поля:
        username (StringField): Поле для выбора имени пользователя
        fio (StringField): Поле для ввода ФИО
        email (StringField): Поле для ввода email
        passwrd (PasswordField): Поле для ввода пароля
        confirm_password (PasswordField): Поле для подтверждения пароля
        submit (SubmitField): Кнопка отправки формы
    """
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    fio = StringField('ФИО:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    passwrd = PasswordField('Пароль:', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Повторите пароль:',
                                     validators=[DataRequired(),
                                                 Length(min=5),
                                                 EqualTo('passwrd')])
    submit = SubmitField('Зарегистрироваться')