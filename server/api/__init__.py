from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

api = Flask(__name__)
api.config.from_object('config.ProductionConfig')
db = SQLAlchemy(api)
migrate = Migrate(api, db)

from api.modules.sql_provider import SQLInitializer
sql_provider = SQLInitializer()(db)

scheduler = APScheduler()
scheduler.init_app(api)
scheduler.start()

store = { 'time_for_rk1': 60, 'time_for_rk2': 60 }

from api.routes import init_controllers
init_controllers(api)