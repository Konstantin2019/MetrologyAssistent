from os import path, getenv
from dotenv import load_dotenv

dir_path = path.abspath(path.dirname(__file__))
dotenv_path = path.join(path.dirname(__file__), '.env')

if path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    UPLOAD_FOLDER = path.join(dir_path, 'api/static/files')
    SECRET_KEY = getenv('SECRET_KEY')
    ADMIN_LOGIN = getenv('ADMIN_LOGIN')
    ADMIN_PASSWORD = getenv('ADMIN_PASSWORD')
    FLASK_ENV = ''
    ENV = FLASK_ENV

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI_DEV') + path.join(dir_path, 'api/static/sqlite_db/tasks.db')
    FLASK_ENV = 'development'
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI =  getenv('SQLALCHEMY_DATABASE_URI_PROD')
    FLASK_ENV = 'production'
    DEBUG = False