from os import path, getenv
from dotenv import load_dotenv

dir_path = path.abspath(path.dirname(__file__))
dotenv_path = path.join(path.dirname(__file__), '.env')

if path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class BaseConfig():
    JSON_AS_ASCII = False
    UPLOAD_FOLDER = path.join(dir_path, 'api/static/files')
    SECRET_KEY = getenv('SECRET_KEY')
    ADMIN_LOGIN = getenv('ADMIN_LOGIN')
    ADMIN_PASSWORD = getenv('ADMIN_PASSWORD')

class DevelopmentConfig(BaseConfig):
    TORTOISE_ORM = {
        "connections": {"default": getenv('DATABASE_URI_DEV') + path.join(dir_path, 'api/static/sqlite_db/tasks.db')},
        "apps": {
            "models": {
                "models": ["api.models", "aerich.models"],
                "default_connection": "default",
                },
            },
        }   
    QUART_ENV = 'development'
    ENV = QUART_ENV
    DEBUG = True

class ProductionConfig(BaseConfig):
    TORTOISE_ORM = {
        "connections": {"default": getenv('DATABASE_URI_PROD')},
        "apps": {
            "models": {
                "models": ["api.models", "aerich.models"],
                "default_connection": "default",
                },
            },
        }   
    QUART_ENV = 'production'
    ENV = QUART_ENV
    DEBUG = False

T_ORM_DEV = DevelopmentConfig.TORTOISE_ORM
T_ORM_PROD = ProductionConfig.TORTOISE_ORM