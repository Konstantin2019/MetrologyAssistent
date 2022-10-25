from api import api, sql_provider, dteachers, dtests
import json
from quart import Blueprint, request, session, make_response
from datetime import datetime
from api.modules.json_utilies import year_to_json, group_to_json, teacher_to_json, test_type_to_json
from api.modules.support_utilies import generate_token
from api.models import Group, Student, Year, Admin
from api.modules.custom_exceptions import ContentError

auth = Blueprint('auth', __name__)

@auth.route('/admin_auth', methods=['POST'])
async def admin_auth():
    credentials = await request.get_json()
    try:
        if credentials['login'] == api.config['ADMIN_LOGIN'] and \
        credentials['password'] == api.config['ADMIN_PASSWORD']:
            tokens = await sql_provider.get_all(Admin)
            tokens_ids = [token.id for token in tokens]
            if len(tokens_ids) > 1:
                await sql_provider.delete_many(Admin, tokens_ids[1:])
            token = generate_token()
            if len(tokens_ids) == 0:
                id = await sql_provider.set(Admin(token=token))
            else:
                id = await sql_provider.update(Admin, 1, {'token': token})
            if not id:
                raise ContentError
            return await make_response(json.dumps(token), 200)
        else:
            return await make_response('Неверная пара логин/пароль!', 401)
    except KeyError:
        return await make_response('Не переданы логин и/или пароль!', 400)  
    except ContentError:
        return await make_response('Не удалось добавить токен в БД!', 400) 

@auth.route('/for_user_auth', methods=['GET'])
async def for_auth():
    current_year = datetime.now().year
    year = await sql_provider.get(Year, key={'year_name': current_year})
    groups = await sql_provider.get_all(Group)
    teachers = [dteachers[key] for key in dteachers]
    tests = [dtests[key] for key in dtests]
    jsonified_year = await year_to_json(year)
    jsonified_groups = [await group_to_json(group) for group in groups]
    jsonified_teachers = [await teacher_to_json(teacher) for teacher in teachers]
    jsonified_tests = [await test_type_to_json(test) for test in tests]
    session['group_load'] = True if groups else False
    return await make_response(json.dumps({'year': jsonified_year, 
                                           'groups': jsonified_groups,
                                           'teachers': jsonified_teachers,
                                           'tests': jsonified_tests}), 200)

@auth.route('/user_auth', methods=['POST'])
async def user_auth():
    if not session['group_load']:
        return await make_response('Аутентификация невозможна!', 500)
    data = await request.get_json()
    if 'email' in data and data['email']:
        email = data['email'].lower()
        student = await sql_provider.get(Student, key={'email': email})
        if student:
            return await make_response(json.dumps(student.id), 200)
    return await make_response('Студент не найден!', 404)