from quart import Quart
from tortoise.contrib.quart import register_tortoise

api = Quart(__name__)
api.config.from_object('config.ProductionConfig')

register_tortoise(
    api,
    config=api.config['TORTOISE_ORM'],
    generate_schemas=False,
)

from api.modules.sql_provider import SQLProvider
sql_provider = SQLProvider()

from api.modules.teachers.teacher import Teacher
dteachers = {
             "potapov": Teacher("Потапов К.Г.", 60, 60, 60),
             "tumakova": Teacher("Тумакова Е.В.", 90, 90, 90)
            }
           
from api.modules.teachers.test_type import TestType
dtests = {
          "rk1": TestType("РК№1"),
          "rk2": TestType("РК№2"),
          "test": TestType("Тест")
         }

from api.controllers.auth_controllers import auth
api.register_blueprint(auth, url_prefix='/api')
from api.controllers.admin_controllers import admin
api.register_blueprint(admin, url_prefix='/api/admin')
from api.controllers.user_controllers import user
api.register_blueprint(user, url_prefix='/api/user')