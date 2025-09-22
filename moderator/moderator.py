import os
import uuid
from flask import (Blueprint, render_template, request,
                   jsonify, flash, redirect, url_for, get_flashed_messages)
from flask_login import login_required, current_user
import config
from database.base import db
from database.models.files_model import File
from database.models.instructions_model import Instruction
from database.models.post_files_model import PostFiles
from database.models.posts_model import Post

# создание blueprint'а для модераторских маршрутов
moderator = Blueprint('moderator', __name__, template_folder='templates', static_folder='static')


def allowed_file(filename):
    """Функция для проверки корректности разрешения файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@moderator.route('/moderator', methods=['GET', 'POST'])
@login_required
def moderator_page():
    """Главная страница модератора"""
    return render_template('moderator/moderator_page.html')


@moderator.route('/all_posts', methods=['GET', 'POST'])
@login_required
def all_posts():
    """Страница со всеми постами в системе"""
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'message': 'Ошибка: ожидался JSON'}), 400

        data = request.get_json()

        post_id = data.get('id')
        action = data.get('action')

        if not post_id or not action:
            return jsonify({'message': 'Ошибка: не хватает параметров'}), 400

        post = Post.query.get_or_404(post_id)

        # Удаление поста
        if action == 'delete':
            db.session.delete(post)
            db.session.commit()
            return jsonify({'message': f'Пост {post_id} успешно удален'}), 200

        # Выложить пост
        elif action == 'publish':
            post.published = 1
            db.session.commit()
            return jsonify({'message': f'Пост {post_id} успешно опубликован'}), 200

        return jsonify({'message': 'Неверное действие'}), 400

    # Поиск поста
    search_query = request.args.get('search', '')
    if search_query:
        posts = Post.query.filter(
            (Post.title.ilike(f"%{search_query}%")) |
            (Post.description.ilike(f"%{search_query}%"))
        ).all()
        if not posts:
            flash('Такой пост не найден', 'error')
    else:
        posts = Post.query.all()
    return render_template('moderator/all_posts.html', posts=posts)


@moderator.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Редактирование выбранного поста"""
    post = Post.query.get_or_404(post_id)
    post_files = PostFiles.query.filter_by(post_id=post_id).all()
    file_ids = [pf.file_id for pf in post_files]
    files = File.query.filter(File.id.in_(file_ids)).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        files_ids_to_add = request.files.getlist('files')
        file_ids_to_delete = request.form.getlist('delete_files')

        error = False
        new_files_data = []

        # Валидация введенных данных
        if not title or not description:
            flash('Заголовок и содержание поста не могут быть пустыми', 'error')
            error = True
        elif len(title) < 3:
            flash('Длина заголовка не может быть меньше 3 символов', 'error')
            error = True
        elif len(description) < 10:
            flash('Длина поста не может быть меньше 10 символов', 'error')
            error = True

        # Проверка файлов на корректность
        for file in files_ids_to_add:
            if file and file.filename:
                if not allowed_file(file.filename):
                    flash("Недопустимый формат файла", "error")
                    error = True
                else:
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(config.UPLOAD_FOLDER, filename)
                    new_files_data.append((file, filename, filepath))

        if not error:
            post.title = title
            post.description = description

            # Удаление выбранных файлов
            if file_ids_to_delete:
                for file_id in file_ids_to_delete:
                    file = File.query.get(file_id)
                    if file:
                        PostFiles.query.filter_by(file_id=file.id, post_id=post_id).delete()
                        db.session.delete(file)

            # Сохранение новых файлов
            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
            for file, filename, filepath in new_files_data:
                file.save(filepath)
                new_file = File(user_id=current_user.id, filename=filename, filepath=filepath)
                db.session.add(new_file)
                db.session.flush()  # получаем ID без коммита

                new_post_files = PostFiles(post_id=post.id, file_id=new_file.id)
                db.session.add(new_post_files)

            db.session.commit()
            flash('Пост успешно обновлен!', 'success')
            return redirect(url_for('.edit_post', post_id=post_id))

    return render_template('moderator/edit_post.html', post=post, post_files=post_files, files=files)


@moderator.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    """Просмотр выбранного поста"""
    post = Post.query.get_or_404(post_id)
    post_files = PostFiles.query.filter_by(post_id=post_id).all()
    file_ids = [pf.file_id for pf in post_files]
    files = File.query.filter(File.id.in_(file_ids)).all()

    return render_template('moderator/post.html', post=post, post_files=post_files, files=files)


@moderator.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    """Добавление нового поста"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        files = request.files.getlist('files')

        # Валидация введенных данных
        if not title or not description:
            flash('Заголовок и содержание поста не могут быть пустыми', 'error')
            return redirect(url_for('.add_post'))
        elif len(title) < 3:
            flash('Длина заголовка не может быть меньше 3 символов', 'error')
            return redirect(url_for('.add_post'))
        elif len(description) < 10:
            flash('Длина поста не может быть меньше 10 символов', 'error')
            return redirect(url_for('.add_post'))

        # Проверка прикрепленных файлов
        for file in files:
            if file and file.filename:
                if not allowed_file(file.filename):
                    flash("Недопустимый формат файла", "error")
                    return redirect(url_for('.add_post'))

        if not get_flashed_messages():
            post = Post(
                title=title,
                description=description,
                published=(1 if current_user.role_id in (1, 3) else 0),
                created_at=db.func.now()
            )
            db.session.add(post)
            db.session.flush()  # Получим post.id до коммита

            for file in files:
                if file and file.filename:
                    filepath = os.path.join(config.UPLOAD_FOLDER, file.filename)
                    file.save(filepath)

                    new_file = File(user_id=current_user.id, filename=file.filename, filepath=filepath)
                    db.session.add(new_file)
                    db.session.flush()

                    new_post_files = PostFiles(post_id=post.id, file_id=new_file.id)
                    db.session.add(new_post_files)

            db.session.commit()
            flash('Пост и файлы успешно добавлены!', 'success')
            return redirect(url_for('.add_post'))
        else:
            flash(get_flashed_messages()[0], 'error')
            return redirect(url_for('.add_post'))

    return render_template('moderator/add_post.html')


@moderator.route('/edit_instruction/<int:instruction_id>', methods=['POST'])
@login_required
def edit_instruction(instruction_id):
    """Редактирование инструкций"""
    instruction = Instruction.query.get_or_404(instruction_id)
    instruction.title = request.form['title']
    instruction.description = request.form['description']
    db.session.commit()
    flash("Инструкция обновлена", "success")

    return redirect(request.referrer or url_for('go_main'))


