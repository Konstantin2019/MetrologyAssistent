from flask import Blueprint, request, session
from flask.helpers import make_response
from datetime import datetime
from api.modules.json_utilies import year_to_json, group_to_json
from api.models.shemas import Group, Student, Year
from api import api, sql_provider, glob
import json

auth = Blueprint('auth', __name__)

@auth.route('/admin_auth', methods=['POST'])
def admin_auth():
    credentials = request.get_json()
    try:
        if credentials['login'] == api.config['ADMIN_LOGIN'] and \
        credentials['password'] == api.config['ADMIN_PASSWORD']:
            glob['admin_status'] = True
            return make_response('ОК', 200)
        else:
            return make_response('Неверная пара логин/пароль!', 401)
    except KeyError:
        return make_response('', 400)  

@auth.route('/for_user_auth', methods=['GET'])
def for_auth():
    current_year = datetime.now().year
    year = sql_provider.query(Year).filter_by(year_name=current_year).scalar()
    groups = sql_provider.get_all(Group)
    if year and len(groups) > 0:
        jsonified_year = year_to_json(year)
        jsonified_groups = [group_to_json(group) for group in groups]
        session['group_load'] = True
        return make_response(json.dumps({'year': jsonified_year, 
                                         'groups': jsonified_groups}), 200)
    else:
        session['group_load'] = False
        return make_response('Отсутствуют учебные группы!', 500)

@auth.route('/user_auth', methods=['POST'])
def user_auth():
    if not session['group_load']:
        return make_response('Аутентификация невозможна!', 500)
    data = request.get_json()
    if 'email' in data and data['email']:
        email = data['email'].lower()
        student = sql_provider.query(Student).filter_by(email=email).scalar()
        if student:
            return make_response(json.dumps(student.id), 200)
    return make_response('Студент не найден!', 404)