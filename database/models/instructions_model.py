from database.base import db


class Instruction(db.Model):
    """
        Модель инструкций(техника безопасности, рабочие инструкции, политика безопасности).
        Поля:
            id (int): Первичный ключ инструкции
            title (str): Название инструкции
            description (str): Описание инструкции
            category_id (int): Ссылка на первичный ключ категории инструкции
            created_at (datetime): Время создания инструкции
            updated_at (datetime): Время обновления инструкции
        Связи:
            category: Связь с категорией инструкции (many-to-one)
    """
    __tablename__ = 'instructions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(10000))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    category = db.relationship('Category', backref='instructions')