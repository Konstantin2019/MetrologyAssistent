from api import api
from api.providers.sql_provider import SQLProvider
from api.helpers.support_utilies import generate_token
from api.helpers.json_utilies import *
from api.models import Admin
from datetime import datetime

async def db_init_handler(provider: SQLProvider):
    teachers = [Teacher("Потапов К.Г.", 60, 60, 60), Teacher("Тумакова Е.В.", 90, 90, 90)]
    await provider.set_many(teachers)
    tests = [TestType("РК№1"), TestType("РК№2"), TestType("Тест")]
    await provider.set_many(tests)

async def admin_auth_handler(provider: SQLProvider, payload: dict):
    if not payload and not 'login' in payload and not 'password' in payload:
        return 'Не переданы логин и/или пароль!', 400
    if payload['login'] == api.config['ADMIN_LOGIN'] and \
    payload['password'] == api.config['ADMIN_PASSWORD']:
        tokens = await provider.get_all(Admin)
        tokens_ids = [token.id for token in tokens]
        if len(tokens_ids) > 1:
            await provider.delete_many(Admin, tokens_ids[1:])
        token = generate_token()
        if len(tokens_ids) == 0:
            id = await provider.set(Admin(token=token))
        else:
            id = await provider.update(Admin, 1, {'token': token})
        if not id:
            return 'Не удалось добавить токен в БД!', 500
        return dumps(token), 200
    else:
        return 'Неверная пара логин/пароль!', 401

async def for_auth_handler(provider: SQLProvider):
    current_year = datetime.now().year
    year = await provider.get(Year, key={'year_name': current_year})
    groups = await provider.get_all(Group)
    teachers = await provider.get_all(Teacher)
    tests = await provider.get_all(TestType)
    jsonified_year = await year_to_json(year)
    jsonified_groups = [await group_to_json(group) for group in groups]
    jsonified_teachers = [await teacher_to_json(teacher) for teacher in teachers]
    jsonified_tests = [await test_type_to_json(test) for test in tests]
    return dumps({'year': jsonified_year, 'groups': jsonified_groups, \
                  'teachers': jsonified_teachers, 'tests': jsonified_tests}), 200, True

async def user_auth_handler(provider: SQLProvider, payload: dict):
    if payload and 'email' in payload and payload['email']:
        email = payload['email'].lower()
        student = await provider.get(Student, key={'email': email})
        if student:
            return dumps(student.id), 200
    return 'Студент не найден!', 404