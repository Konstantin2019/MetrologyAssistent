from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

api = Flask(__name__)
api.config.from_object('config.ProductionConfig')
db = SQLAlchemy(api)
migrate = Migrate(api, db)

entry = Blueprint('entry', __name__)
admin = Blueprint('admin', __name__)
user = Blueprint('user', __name__, static_folder=api.config['UPLOAD_FOLDER'])
api.register_blueprint(entry, url_prefix='/api')
api.register_blueprint(admin, url_prefix='/api/admin')
api.register_blueprint(user, url_prefix='/api/user')

from api.modules.sql_provider import SQLInitializer
sql_provider = SQLInitializer()(db)

store = { 'time_for_rk1': 60, 'time_for_rk2': 60, 'time_for_test': 80 }

from api.routes import init_endpoints
init_endpoints(api)