import calendar
from datetime import date, timedelta
from deep_translator import GoogleTranslator
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages
from flask_login import login_required, current_user
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from werkzeug.security import generate_password_hash
from database.base import db
from database.models.posts_model import Post
from database.models.users_model import User
from database.models.vacation_days_model import VacationDays
from flask import send_file
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle, Paragraph
from io import BytesIO
from datetime import datetime

# Создание blueprint'а для администраторских маршрутов
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin_page():
    """Главна страница администратора"""
    if current_user.role_id == 1:
        users_list_vac = User.query.all()
        search_query = request.args.get('search', '')
        if search_query:
            users = User.query.filter(
                (User.username.ilike(f"%{search_query}%")) |
                (User.fio.ilike(f"%{search_query}%"))
            ).all()
            if users:
                user_ids = [user.id for user in users]
                vacation_user = VacationDays.query.filter(VacationDays.user_id.in_(user_ids)).all()
            else:
                users = []
                vacation_user = []
                flash('Такой пользователь не найден', 'error')
        else:
            vacation_user = []
            users = []

        # Формирование данных для календаря с отпусками сотрудников
        months = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
                  7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

        year = request.args.get("year", default=datetime.now().year, type=int)
        month = request.args.get("month", default=datetime.now().month, type=int)

        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])

        vacations = VacationDays.query.filter(VacationDays.startt.between(first_day, last_day)).all()

        available_years = list(range(2020, 2031))
        available_months = months.items()

        return render_template(
            'admin/admin_page.html',
            users=users,
            users_list_vac=users_list_vac,
            vacations=vacations,
            vacation_user=vacation_user,
            year=year,
            month=month,
            months=months,
            available_years=available_years,
            available_months=available_months
        )
    else:
        flash('У вас нет прав доступа к этой странице', 'error')
        return redirect(url_for('user.main'))


@admin.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    """Добавление нового пользователя"""
    if request.method == 'POST':
        # Валидация введенных данных
        if request.form['fio'] and request.form['password'] and request.form['username']:
            username = request.form['username']
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                flash('Такое имя пользователя уже существует', 'error')

            if any(b.isdigit() for b in request.form['fio']):
                flash('В ФИО не могут содержаться цифры', 'error')

            new_email = request.form['email']
            try:
                validate_email(new_email)
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user:
                    flash('Пользователь с таким email уже существует', 'error')
            except EmailNotValidError as e:
                error_message = str(e)
                translated_error = GoogleTranslator(source='en', target='ru').translate(error_message)
                flash(translated_error, 'error')

            if not request.form['phone_number'].isdigit():
                flash('Номер телефона должен быть введен цифрами', 'error')
            if len(request.form['phone_number']) != 11:
                flash('Номер телефона состоит из 11 цифр', 'error')

            today = date.today()
            if request.form['date_of_birth'] == '':
                data = datetime.strptime("1900-01-01", "%Y-%m-%d").date()
            else:
                data = datetime.strptime(request.form['date_of_birth'], "%Y-%m-%d").date()
            time_difference = today - data
            if time_difference <= timedelta(days=365 * 18 + 18 / 4):
                flash('Возраст не может быть меньше 18 лет', 'error')

            if len(request.form['password']) < 5:
                flash('Длина пароля не может быть меньше 5 символов', 'error')
            if not any(b.isdigit() for b in request.form['password']):
                flash('Пароль должен содержать цифры', 'error')
            else:
                hashed_password = generate_password_hash(request.form['password'])
        else:
            flash('ФИО, пароль и имя пользователя должны быть заполнены', 'error')

        if not get_flashed_messages():
            user = User(
                username=request.form['username'],
                fio=request.form['fio'],
                passwrd=hashed_password,
                date_of_birth=data,
                phone_number=request.form['phone_number'],
                email=request.form['email'],
                role_id=request.form['role_id']
            )
            db.session.add(user)
            db.session.commit()
            flash('Новый пользователь успешно добавлен!', 'success')
        else:
            flash(get_flashed_messages()[0], 'error')
        return redirect(url_for('.add_user'))

    return render_template('admin/add_user.html')


@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Редактирование существующего пользователя"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Валидация введенных значений
        if not request.form['fio'] or not request.form['password'] or not request.form['username']:
            flash('ФИО, пароль и имя пользователя не могут быть пустыми', 'error')
        else:
            existing_username = User.query.filter_by(username=request.form['username']).first()
            if existing_username:
                if existing_username.id != user_id:
                    flash('Данный пользователь уже существует', 'error')

            if any(b.isdigit() for b in request.form['fio']):
                flash('В ФИО не могут содержаться цифры', 'error')

            new_email = request.form['email']
            try:
                validate_email(new_email)
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user:
                    if existing_user.id != user_id:
                        flash('Пользователь с таким email уже существует', 'error')
            except EmailNotValidError as e:
                error_message = str(e)
                translated_error = GoogleTranslator(source='en', target='ru').translate(error_message)
                flash(translated_error, 'error')

            if not request.form['phone_number'].isdigit():
                flash('Номер телефона должен быть введен цифрами', 'error')
            if len(request.form['phone_number']) != 11:
                flash('Номер телефона состоит из 11 цифр', 'error')

            today = date.today()
            if request.form['date_of_birth'] == '':
                data = datetime.strptime("1900-01-01", "%Y-%m-%d").date()
            else:
                data = datetime.strptime(request.form['date_of_birth'], "%Y-%m-%d").date()
            time_difference = today - data
            if time_difference <= timedelta(days=365 * 18 + 18 / 4):
                flash('Возраст не может быть меньше 18 лет', 'error')

            if len(request.form['password']) < 5:
                flash('Длина пароля не может быть меньше 5 символов', 'error')
            if not any(b.isdigit() for b in request.form['password']):
                flash('Пароль должен содержать цифры', 'error')
            else:
                hashed_password = generate_password_hash(request.form['password'])

        if not get_flashed_messages():
            user.username = request.form['username']
            user.email = request.form['email']
            user.fio = request.form['fio']
            user.phone = request.form['phone_number']
            user.role_id = request.form['role_id']
            user.passwrd = hashed_password
            user.date_of_birth = data
            db.session.commit()
            flash('Данные пользователя успешно обновлены!', 'success')
        else:
            flash(get_flashed_messages()[0], 'error')
        return redirect(url_for('.edit_user', user_id=user.id))

    return render_template('admin/edit_user.html', user=user)



@admin.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    """Удаление пользователя"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('.admin_page'))


@admin.route('/reject_vacation/<int:vacation_id>', methods=['GET', 'POST'])
@login_required
def reject_vacation(vacation_id):
    """Отклонить заявку на отпуск"""
    vacation = VacationDays.query.get_or_404(vacation_id)
    db.session.delete(vacation)
    db.session.commit()
    flash('Запрос на отпуск успешно удален!', 'success')
    return redirect(url_for('.admin_page'))


@admin.route('/create_vacation', methods=['GET', 'POST'])
@login_required
def create_vacation():
    """Создание заявки на отпуск"""
    users = User.query.all()

    if request.method == 'POST':
        user_id = request.form['user_id']

        today = date.today()
        # Валидация введенных дат
        if not request.form['startt'] or not request.form['endd']:
            flash('Заполните поля с датами', 'error')
        else:
            data_start = datetime.strptime(request.form['startt'], '%Y-%m-%d').date()
            data_end = datetime.strptime(request.form['endd'], '%Y-%m-%d').date()
            if data_start < today or data_end < today:
                flash('Дата не может быть в прошлом', 'error')
            if data_start > data_end:
                flash('Дата начала не может быть позднее даты конца', 'error')

        if not get_flashed_messages():
            vacation = VacationDays(
                user_id=user_id,
                startt=data_start,
                endd=data_end
            )
            db.session.add(vacation)
            db.session.commit()
            flash(f'Запрос на отпуск создан!', 'success')
            return redirect('create_vacation')
        else:
            flash(get_flashed_messages()[0], 'error')
            return redirect('create_vacation')

    return render_template('admin/create_vacation.html', users=users)


@admin.route('/accept_vacation/<int:vacation_id>', methods=['GET', 'POST'])
@login_required
def accept_vacation(vacation_id):
    """Одобрение заявки на отпуск"""
    vacation = VacationDays.query.get_or_404(vacation_id)
    vacation.published = 1
    db.session.commit()
    flash(f'Запрос на отпуск № {vacation_id} одобрен!', 'success')
    return redirect(url_for('.admin_page'))


#Установка шрифта для pdf-документа
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/uploads/DejaVuSans.ttf'))


@admin.route('/posts_report')
@login_required
def posts_report():
    """Генерация pdf-отчета о постах"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    top_margin = 50
    left_margin = 50

    y = height - top_margin

    # Заголовок
    p.setFont("DejaVuSans", 18)
    p.setFillColor(colors.HexColor("#389fc6"))
    p.drawString(left_margin, y, "Отчёт по постам")
    y -= 25

    # Дата формирования
    p.setFont("DejaVuSans", 10)
    p.setFillColor(colors.black)
    p.drawString(left_margin, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 25

    # Стили Paragraph
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "DejaVuSans"
    style.fontSize = 9
    style.leading = 12

    # Получение данных
    posts = Post.query.order_by(Post.created_at.desc()).all()
    data = [["Заголовок", "Описание", "Дата создания", "Статус"]]
    status_colors = []

    for post in posts:
        status_text = "Опубликован" if post.published else "Черновик"
        status_color = colors.HexColor("#b2f2bb") if post.published else colors.HexColor("#ffb3b3")

        title = Paragraph(post.title[:35].replace("\n", "<br/>") + ("..." if len(post.title) >= 35 else ""), style)
        description = Paragraph(post.description[:70].replace("\n", "<br/>") + ("..." if len(post.description) >= 70 else ""), style)
        created = Paragraph(post.created_at.strftime("%d.%m.%Y %H:%M"), style)
        status_paragraph = Paragraph(status_text, style)

        data.append([title, description, created, status_paragraph])
        status_colors.append(status_color)

    # Размеры таблицы
    table_width = width - 2 * left_margin
    col_widths = [table_width * w for w in [0.27, 0.47, 0.15, 0.15]]

    table = Table(data, colWidths=col_widths, repeatRows=1)

    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#389fc6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEADING", (0, 0), (-1, -1), 12),
    ]

    for row_index, color in enumerate(status_colors, start=1):
        style_commands.append(("BACKGROUND", (3, row_index), (3, row_index), color))

    table.setStyle(TableStyle(style_commands))

    # Подсчёт высоты таблицы
    row_height = 20
    table_height = len(data) * row_height

    # Расположение таблицы ниже заголовка и даты
    table_y = y - table_height
    if table_y < 100:
        table_y = 100  # Не даём таблице наехать на футер

    table.wrapOn(p, width, height)
    table_height = table._height  # Получаем фактическую высоту таблицы
    table.drawOn(p, left_margin, y - table_height)
    y -= table_height + 40

    # Подпись
    p.setFont("DejaVuSans", 10)
    p.setFillColor(colors.black)
    p.drawString(left_margin, y, f"Сформировал отчёт: {current_user.fio}")

    # Футер
    p.setFont("DejaVuSans", 8)
    p.setFillColor(colors.grey)
    p.drawString(left_margin, 20, 'Сгенерировано автоматически • Информационно-справочная система "Предприятие"')
    p.drawRightString(width - left_margin, 20, "Стр. 1")

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="posts_report.pdf", mimetype="application/pdf")


@admin.route('/users_report')
@login_required
def users_report():
    """Генерация pdf-отчета о пользователях"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    y = height - 50

    # Заголовок
    p.setFont("DejaVuSans", 18)
    p.setFillColor(colors.HexColor("#389fc6"))
    p.drawString(50, y, "Отчёт по пользователям")
    y -= 25

    # Дата
    p.setFont("DejaVuSans", 10)
    p.setFillColor(colors.black)
    p.drawString(50, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 30

    # Стили Paragraph
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "DejaVuSans"
    style.fontSize = 9
    style.leading = 12

    # Данные
    users = User.query.order_by(User.created_at.desc()).all()
    data = [["ФИО", "Дата рождения", "Телефон", "Email", "Роль", "Дата регистрации"]]

    for user in users:
        fio = Paragraph(user.fio, style)
        dob = Paragraph(user.date_of_birth.strftime("%d.%m.%Y") if user.date_of_birth else "-", style)
        phone = Paragraph(user.phone_number if user.phone_number else "-", style)
        email = Paragraph(user.email if user.email else "-", style)
        role = Paragraph(user.role.role_name if user.role else "-", style)
        reg_date = Paragraph(user.created_at.strftime("%d.%m.%Y %H:%M"), style)

        data.append([fio, dob, phone, email, role, reg_date])

    # Размеры
    table_width = width - 100
    col_widths = [table_width * w for w in [0.23, 0.13, 0.15, 0.21, 0.13, 0.15]]

    # Таблица
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#389fc6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
    ]))

    # Вывод таблицы
    table.wrapOn(p, width, height)
    table_height = len(data) * 18
    table.drawOn(p, 50, y - table_height)
    y -= table_height + 40

    # Подпись
    p.setFont("DejaVuSans", 10)
    p.setFillColor(colors.black)
    p.drawString(50, y, f"Сформировал отчёт: {current_user.fio}")

    # Футер
    p.setFont("DejaVuSans", 8)
    p.setFillColor(colors.grey)
    p.drawString(50, 20, 'Сгенерировано автоматически • Информационно-справочная система "Предприятие"')
    p.drawRightString(width - 50, 20, "Стр. 1")

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="users_report.pdf", mimetype="application/pdf")


@admin.route('/vacations_report')
@login_required
def vacations_report():
    """Генерация pdf-отчета об отпусках"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    y = height - 50

    # Заголовок
    p.setFont("DejaVuSans", 18)
    p.setFillColor(colors.HexColor("#389fc6"))
    p.drawString(50, y, "Отчёт по отпускам")
    y -= 25

    # Дата формирования
    p.setFont("DejaVuSans", 10)
    p.setFillColor(colors.black)
    p.drawString(50, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 30

    # Paragraph стиль
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "DejaVuSans"
    style.fontSize = 9
    style.leading = 12

    # Заголовки таблицы
    data = [["Сотрудник", "Начало", "Окончание", "Длительность (дн.)", "Статус"]]
    status_colors = []

    today = date.today()
    vacations = VacationDays.query.join(User).order_by(VacationDays.startt.desc()).all()

    for v in vacations:
        fio = Paragraph(v.users.fio if v.users else "-", style)
        start = Paragraph(v.startt.strftime("%d.%m.%Y") if v.startt else "-", style)
        end = Paragraph(v.endd.strftime("%d.%m.%Y") if v.endd else "-", style)

        # Расчёт длительности
        if v.startt and v.endd:
            duration = (v.endd.date() - v.startt.date()).days + 1
        else:
            duration = "-"

        duration_paragraph = Paragraph(str(duration), style)

        # Статус
        if not v.published:
            status = "Не одобрен"
            color = colors.HexColor("#ffd6d6")
        elif v.startt.date() > today:
            status = "Запланирован"
            color = colors.HexColor("#d6f0ff")
        elif v.startt.date() <= today <= v.endd.date():
            status = "Текущий"
            color = colors.HexColor("#b2f2bb")
        else:
            status = "Прошедший"
            color = colors.HexColor("#e6e6e6")

        status_paragraph = Paragraph(status, style)

        data.append([fio, start, end, duration_paragraph, status_paragraph])
        status_colors.append(color)

    # Колонки и стили
    table_width = width - 100
    col_widths = [table_width * w for w in [0.30, 0.17, 0.17, 0.17, 0.17]]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#389fc6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEADING", (0, 0), (-1, -1), 12),
    ]

    for i, color in enumerate(status_colors, start=1):
        style_commands.append(("BACKGROUND", (4, i), (4, i), color))  # колонка статуса

    table.setStyle(TableStyle(style_commands))

    # Отрисовка таблицы
    table.wrapOn(p, width, height)
    table_height = len(data) * 18
    table.drawOn(p, 50, y - table_height)
    y -= table_height + 40

    # Подпись
    p.setFont("DejaVuSans", 10)
    p.setFillColor(colors.black)
    p.drawString(50, y, f"Сформировал отчёт: {current_user.fio}")

    # Футер
    p.setFont("DejaVuSans", 8)
    p.setFillColor(colors.grey)
    p.drawString(50, 20, 'Сгенерировано автоматически • Информационно-справочная система "Предприятие"')
    p.drawRightString(width - 50, 20, "Стр. 1")

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="vacations_report.pdf", mimetype="application/pdf")



