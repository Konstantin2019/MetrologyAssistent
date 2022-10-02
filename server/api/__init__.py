from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

api = Flask(__name__)
api.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(api)
migrate = Migrate(api, db)
login_manager = LoginManager(api)

from api.modules.sql_provider import SQLInitializer
sql_provider = SQLInitializer()(db)

glob = { 'time_for_rk1': 60, 'time_for_rk2': 60, 'time_for_test': 80, 'admin_status': False }

from api.auth import auth
api.register_blueprint(auth, url_prefix='/api')
from api.admin import admin
api.register_blueprint(admin, url_prefix='/api/admin')
from api.user import user
api.register_blueprint(user, url_prefix='/api/user')