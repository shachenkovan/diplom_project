from database.base import db

class VacationDays(db.Model):
    """
        Модель отпуска
        Поля:
            id (int): Первичный ключ отпуска
            user_id (int): Связь с пользователем
            startt (datetime): Дата начала отпуска
            endd (datetime): Дата конца отпуска
            published (bool): Флаг, отмечающий одобрен ли отпуск администратором
        Связи:
            users: Связь с пользователем (one-to-many)
    """
    __tablename__ = 'vacation_days'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    startt = db.Column(db.DateTime)
    endd = db.Column(db.DateTime)
    published = db.Column(db.Boolean, default=False)

    users = db.relationship('User', back_populates='vacations')

