from quart import Quart
from tortoise.contrib.quart import register_tortoise

api = Quart(__name__)
api.config.from_object('config.DevelopmentConfig')

register_tortoise(
    api,
    config=api.config['TORTOISE_ORM'],
    generate_schemas=False,
)

from api.modules.sql_provider import SQLProvider
sql_provider = SQLProvider()

server_const = { 'time_for_rk1': 60, 'time_for_rk2': 60, 'time_for_test': 80 }

from api.controllers.auth_controllers import auth
api.register_blueprint(auth, url_prefix='/api')
from api.controllers.admin_controllers import admin
api.register_blueprint(admin, url_prefix='/api/admin')
from api.controllers.user_controllers import user
api.register_blueprint(user, url_prefix='/api/user')