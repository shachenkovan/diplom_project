from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    """
        Базовый класс для всех моделей SQLAlchemy.
        Предоставляет общие функциональности и метаданные для всех моделей.
    """
    pass

db = SQLAlchemy(model_class=Base)


from database.models.users_model import User
from database.models.vacation_days_model import VacationDays
from database.models.files_model import File
from database.models.roles_model import Role
from database.models.post_files_model import PostFiles
from database.models.posts_model import Post
from database.models.instructions_model import Instruction
from database.models.categories_model import Category