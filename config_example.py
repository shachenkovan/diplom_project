"""
Конфигурация Flask приложения.
Этот файл содержит настройки базы данных, безопасности и загрузки файлов.
Для запуска замените значения на реальные.
"""

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/db_name' # укажите вашу бд
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'your-secret-key' # укажите свой секретный ключ
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
UPLOAD_FOLDER= 'static/uploads'