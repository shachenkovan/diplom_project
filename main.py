import os
from flask import (Flask, render_template, flash,
                   redirect, url_for, send_from_directory)
from flask_login import (LoginManager, login_user,
                         login_required, logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from database.base import db
from database.models.files_model import File
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY, UPLOAD_FOLDER
from database.models.users_model import User
from email_validator import validate_email, EmailNotValidError
from deep_translator import GoogleTranslator
from forms import AutoForm, RegForm
from admin.admin import admin
from user.user import user
from moderator.moderator import moderator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

# Регистрация blueprint'ов
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(moderator, url_prefix="/moderator")
app.register_blueprint(user, url_prefix="/user")

# Инициализация менеджера авторизации
login_manager = LoginManager(app)
login_manager.login_view = 'auto'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя по ID для Flask-Login"""
    return User.query.get(int(user_id))


@app.route('/')
def welcome():
    """Главная страница приложения"""
    return render_template('html/welcome.html')


@app.route('/auto', methods=['GET', 'POST'])
def auto():
    """Страница авторизации с поддержкой remember-me"""
    # Если пользователь уже авторизован (благодаря remember-me cookie)
    if current_user.is_authenticated:
        return redirect_to_user_page(current_user)

    form_auto = AutoForm()

    if form_auto.validate_on_submit():
        email = form_auto.email.data
        password = form_auto.passwrd.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.passwrd, password):
            login_user(user)
            return redirect_to_user_page(user)
        else:
            flash('Неверный email или пароль', 'error')

    return render_template('html/auto.html', form=form_auto)


def redirect_to_user_page(user):
    """Перенаправление пользователя на соответствующую страницу по роли"""
    if user.role_id == 1:
        return redirect(url_for('admin.admin_page'))
    elif user.role_id == 3:
        return redirect(url_for('moderator.moderator_page'))
    else:
        return redirect(url_for('user.main'))


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    """Страница регистрации нового пользователя"""
    form_reg = RegForm()

    if form_reg.validate_on_submit():
        errors = validate_registration_data(form_reg)

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            create_new_user(form_reg)
            flash('Регистрация прошла успешно. Пожалуйста, авторизуйтесь', 'success')
            return redirect(url_for('auto'))

    return render_template('html/reg.html', form=form_reg)


def validate_registration_data(form):
    """Валидация данных регистрации"""
    errors = []

    username = form.username.data
    if User.query.filter_by(username=username).first():
        errors.append('Такое имя пользователя уже существует')

    email = form.email.data
    try:
        validate_email(email)
        if User.query.filter_by(email=email).first():
            errors.append('Пользователь с таким email уже существует')
    except EmailNotValidError as e:
        translated_error = GoogleTranslator(source='en', target='ru').translate(str(e))
        errors.append(translated_error)

    password = form.passwrd.data
    if len(password) < 5:
        errors.append('Длина пароля не может быть меньше 5 символов')
    elif not any(char.isdigit() for char in password):
        errors.append('Пароль должен содержать цифры')
    elif password != form.confirm_password.data:
        errors.append('Пароли не совпадают')

    fio = form.fio.data
    if any(char.isdigit() for char in fio):
        errors.append('В ФИО не могут содержаться цифры')

    return errors


def create_new_user(form):
    """Создание нового пользователя в базе данных"""
    hashed_password = generate_password_hash(form.passwrd.data)
    new_user = User(
        username=form.username.data,
        email=form.email.data,
        passwrd=hashed_password,
        fio=form.fio.data,
        role_id=2 # по умолчанию всегда создается обычный пользователь
    )
    db.session.add(new_user)
    db.session.commit()


@app.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('welcome'))


@app.route('/uploads/<filename>')
@login_required
def download_file(filename):
    """Скачивание файла"""
    file = File.query.filter_by(filename=filename).first_or_404()

    if os.path.exists(file.filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        flash("Файл не найден", "error")
        return redirect(url_for('go_main'))


@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    """Удаление файла"""
    file = File.query.get_or_404(file_id)

    if file.user_id == current_user.id:
        if os.path.isfile(file.filepath):
            os.remove(file.filepath)
        db.session.delete(file)
        db.session.commit()
        flash("Файл удален", "success")
    else:
        flash("Ошибка при удалении файла", "error")

    return redirect(url_for('go_main'))


@app.route('/go_main')
@login_required
def go_main():
    """Перенаправление на главную страницу по роли"""
    return redirect_to_user_page(current_user)


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        finally:
            db.session.remove()
    app.run(debug=True)