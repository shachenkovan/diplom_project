from datetime import date, datetime, timedelta
from deep_translator import GoogleTranslator
from email_validator import validate_email, EmailNotValidError
from flask import (Blueprint, render_template, request, flash,
                   get_flashed_messages, redirect, url_for)
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from database.base import db
from database.models.categories_model import Category
from database.models.instructions_model import Instruction
from database.models.posts_model import Post
from database.models.users_model import User
from database.models.vacation_days_model import VacationDays

# создание blueprint'а для пользовательских маршрутов
user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@user.route('/main')
@login_required
def main():
    """Главная страница пользователя с новостной лентой"""
    search_query = request.args.get('search', '')
    if search_query:
        # Поиск постов по заголовку или описанию
        posts = Post.query.filter(
            (Post.title.ilike(f"%{search_query}%")) |
            (Post.description.ilike(f"%{search_query}%"))
        ).all()
        if not posts:
            flash('Такой пост не найден', 'error')
    else:
        posts = Post.query.all()

    return render_template('user/main.html', user=current_user, posts=posts)


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Профиль пользователя, просмотр и редактирование своих данных"""
    if request.method == 'POST':
        # Валидация ФИО пользователя
        if 'fio' in request.form:
            if request.form['fio'] == '':
                flash('ФИО не может быть пустым', 'error')
            elif any(b.isdigit() for b in request.form['fio']):
                flash('В ФИО не могут содержаться цифры', 'error')
            else:
                current_user.fio = request.form['fio']

        # Валидация адреса электронной почты
        if 'email' in request.form:
            new_email = request.form['email']
            try:
                validate_email(new_email)
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != current_user.id:
                    flash('Пользователь с таким email уже существует', 'error')
                else:
                    current_user.email = new_email
            except EmailNotValidError as e:
                error_message = str(e)
                # перевод на русский язык ошибки о некорректном адресе электронной почты
                translated_error = GoogleTranslator(source='en', target='ru').translate(error_message)
                flash(translated_error, 'error')

        # Валидация пароля
        if 'password' in request.form:
            if request.form['password'] != '':
                if len(request.form['password']) < 5:
                    flash('Длина пароля должна быть больше 5 символов', 'error')
                elif not any(b.isdigit() for b in request.form['password']):
                    flash('Пароль должен содержать цифры', 'error')
                elif check_password_hash(current_user.passwrd, request.form['password']):
                    flash('Пароль не может совпадать с предыдущим', 'error')
                else:
                    current_user.passwrd = generate_password_hash(request.form['password'])

        # Валидация номера телефона
        if 'phone' in request.form:
            if not request.form['phone'].isdigit():
                flash('Номер телефона должен быть введен цифрами', 'error')
            elif len(request.form['phone']) != 11:
                flash('Номер телефона состоит из 11 цифр', 'error')
            else:
                current_user.phone_number = request.form['phone']

        # Валидация даты рождения
        if 'date-birth' in request.form:
            if request.form['date-birth'] == '':
                flash('Дата рождения не может быть пустой', 'error')
            else:
                today = date.today()
                data = datetime.strptime(request.form['date-birth'], "%Y-%m-%d").date()
                time_difference = today - data
                # проверка соответствия возраста 18 годам с учетом високосных годов
                if time_difference > timedelta(days=365 * 18 + 18 / 4):
                    current_user.date_of_birth = request.form['date-birth']
                else:
                    flash('Возраст не может быть меньше 18 лет', 'error')

        if not get_flashed_messages():
            db.session.commit()
            flash('Данные успешно обновлены!', 'success')
        else:
            flash(get_flashed_messages()[0], 'error')
        return redirect(url_for('.user_profile'))

    return render_template('user/user-profile.html', title='Редактировать профиль', user=current_user)



@user.route('/request_vacation', methods=['GET', 'POST'])
@login_required
def request_vacation():
    """Отправка заявки на отпуск"""
    vacation_days = VacationDays.query.all()
    if request.method == 'POST':
        today = date.today()
        # Проверка пустых полей
        if not request.form['startt'] or not request.form['endd']:
            flash('Заполните поля с датами', 'error')
        else:
            data_start = datetime.strptime(request.form['startt'], '%Y-%m-%d').date()
            data_end = datetime.strptime(request.form['endd'], '%Y-%m-%d').date()
            # Проверка корректности введеных дат
            if data_start < today or data_end < today:
                flash('Дата не может быть в прошлом', 'error')
            if data_start > data_end:
                flash('Дата начала не может быть позднее даты конца', 'error')

        if not get_flashed_messages():
            vacation = VacationDays(
                user_id=current_user.id,
                startt=data_start,
                endd=data_end
            )
            db.session.add(vacation)
            db.session.commit()
            flash(f'Запрос на отпуск отправлен!', 'success')
            return redirect(url_for('.request_vacation'))

    return render_template('user/request_vacation.html', vacation_days=vacation_days, date=date)


@user.route('/texnika_safety')
@login_required
def texnika_safety():
    """Просмотр техники безопасности"""
    category = Category.query.filter_by(title='Техника безопасности').first()
    instructions = Instruction.query.filter_by(category_id=category.id).all()
    return render_template(
        'user/base_instruction_category.html',
        instructions=instructions,
        category=category.title
    )


@user.route('/security_policy')
@login_required
def security_policy():
    """Просмотр политики безопасности"""
    category = Category.query.filter_by(title='Политика безопасности').first()
    instructions = Instruction.query.filter_by(category_id=category.id).all()
    return render_template(
        'user/base_instruction_category.html',
        instructions=instructions,
        category=category.title
    )


@user.route('/work_instructions')
@login_required
def work_instructions():
    """Просмотр рабочих инструкций"""
    category = Category.query.filter_by(title='Рабочие инструкции').first()
    instructions = Instruction.query.filter_by(category_id=category.id).all()
    return render_template(
        'user/base_instruction_category.html',
        instructions=instructions,
        category=category.title
    )

