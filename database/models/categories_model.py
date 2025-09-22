from database.base import db


class Category(db.Model):
    """
        Модель категории инструкций для их группировки.
        Поля:
            id (int): Первичный ключ категории
            title (str): Описание категории
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
