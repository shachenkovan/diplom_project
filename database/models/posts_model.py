from database.base import db

class Post(db.Model):
    """
        Модель постов в системе
        Поля:
            id (int): Первичный ключ поста
            title (str): Заголовок поста
            description (str): Описание поста
            created_at (datetime): Время создания поста
            published (bool): Флаг, отмечающий выложен ли файл на новостную ленту
        Связи:
            post_files: Связь со связующей таблицей между постами и файлами (one-to-many)
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(10000))
    created_at = db.Column(db.DateTime, default=db.func.now())
    published = db.Column(db.Boolean, default=False)

    post_files = db.relationship('PostFiles', back_populates='post')
