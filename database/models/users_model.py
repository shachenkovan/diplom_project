from database.base import db

class User(db.Model):
    """
        Модель пользователя
        Поля:
            id (int): Первичный ключ пользователя
            username (str): Псевдоним пользователя
            passwrd (str): Пароль пользователя
            fio (str): ФИО пользователя
            date_of_birth (datetime): Дата рождения пользователя
            phone_number (str): Номер телефона пользователя
            email (str): Адрес электронной почты пользователя
            role_id (int): Ссылка на первичный ключ роли пользователя
            created_at (datetime): Дата создания пользователя
            updated_at (datetime): Дата обновления данных о пользователе
        Связи:
            role: Связь с ролями (many-to-one)
            vacations: Связь с отпусками (one-to-many)
            files: Связь с файлами (one-to-many)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    passwrd = db.Column(db.String(255), nullable=False)
    fio = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(11))
    email = db.Column(db.String(100), nullable=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    role = db.relationship('Role', back_populates='users')
    vacations = db.relationship('VacationDays', back_populates='users')
    files = db.relationship('File', back_populates='user')


    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
