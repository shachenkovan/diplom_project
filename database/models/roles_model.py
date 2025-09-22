from database.base import db


class Role(db.Model):
    """
        Модель ролей пользователей
        Поля:
            id (int): Первичный ключ роли
            role_name (str): Название роли
        Связи:
            users: Связь с пользователем (one-to-many)
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)

    users = db.relationship('User', back_populates='role')