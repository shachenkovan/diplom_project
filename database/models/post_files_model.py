from database.base import db

class PostFiles(db.Model):
    """
        Модель связующей таблицы между постами и файлами, для устранения связи many-to-many
        Поля:
            id (int): Первичный ключ свящующей таблицы
            file_id (int): Ссылка на первичный ключ файла
            post_id (int): Ссылка на первичный ключ поста
        Связи:
            file: Связь с файлом (many-to-one)
            post: Связь с постом (many-to-one)
    """
    __tablename__ = 'post_files'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    file = db.relationship('File', back_populates='post_files')
    post = db.relationship('Post', back_populates='post_files')
