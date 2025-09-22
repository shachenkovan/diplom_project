from database.base import db

class File(db.Model):
    """
        Модель файлов в системе.
        Поля:
            id (int): Первичный ключ файла
            user_id (int): Ссылка на первичный ключ пользователя, добавившего файл
            filepath (str): Путь к файлу
            filename (str): Название файла
        Связи:
            user: Связь с пользователем, который добавил этот файл (many-to-one)
            post_files: Связующая таблица между файлами и постами для устранения связи many-to-many (one-to-many)
    """
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', back_populates='files')
    post_files = db.relationship('PostFiles', back_populates='file')
