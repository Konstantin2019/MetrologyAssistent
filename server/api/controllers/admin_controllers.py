import asyncio
import json
from tortoise.expressions import Q
from quart import Blueprint, request, make_response
from werkzeug import Response
from datetime import datetime
from api.modules.json_utilies import year_to_json, group_to_json, student_to_json, question_to_json, test_type_to_json
from api.models import Group, Student, Year, RK1, RK2, Test, Admin, TestType
from api import sql_provider
from api.modules.custom_exceptions import ContentError

admin = Blueprint('admin', __name__)

@admin.before_request
async def admin_middleware():
    if request.method == "OPTIONS":
        return make_response('', 200)
    token = request.headers.get('token')
    if token:
        admin: Admin = await sql_provider.get(Admin, 1)
        if admin.token == token:
            return None
    return make_response('Не авторизован!', 401)

@admin.after_request
def response_wrapper(response: Response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "token")
    return response

@admin.route('/', methods=['GET'])
async def admin_index():
    years, groups, students, tests = await asyncio.gather(sql_provider.get_all(Year), \
                                                          sql_provider.get_all(Group), \
                                                          sql_provider.get_all(Student),\
                                                          sql_provider.get_all(TestType))
    jsonfied_years = [year_to_json(year) for year in years]
    jsonfied_groups = [group_to_json(group) for group in groups]
    jsonfied_students = [student_to_json(student) for student in students]
    jsonified_tests = [test_type_to_json(test) for test in tests]
    return make_response(json.dumps({'years': jsonfied_years, 
                                         'groups': jsonfied_groups, 
                                         'students': jsonfied_students,
                                         'tests': jsonified_tests}), 200)     
    
@admin.route('/create_group', methods=['POST'])
async def create_group():
    data = await request.get_json()
    try:
        if len(data['group_name']) > 0:
            current_year = datetime.now().year
            year_record = await sql_provider.get(Year, Q(year_name=current_year))
            if year_record:
                group_id = await sql_provider.set(Group(group_name=data['group_name'], year_id=year_record.id))
            else:
                year = Year(year_name=current_year)
                new_year_id = await sql_provider.set(year)
                group_id = await sql_provider.set(Group(group_name=data['group_name'], year_id=new_year_id))
            return make_response(json.dumps(group_id), 201)
        else:
            raise ContentError
    except (KeyError, ContentError):
        return make_response('Невалидные данные для создания группы!', 400)   
    
@admin.route('/del_group/<int:group_id>', methods=['DELETE'])
async def del_group(group_id):
    id = await sql_provider.delete(Group, group_id)
    if id:
        return make_response(json.dumps(id), 200)
    else:
        return make_response('Передан неверный id группы!', 400)

@admin.route('/add_students', methods=['POST'])
async def add_students():
    data = await request.get_json()
    try:
        if type(data['students']) is not list:
            student = Student(surname=data['students']['surname'], name=data['students']['name'], \
                              patronymic=data['students']['patronymic'],
                              email=data['students']['email'], group_id=data['students']['group_id'])
            if (student.surname or student.name or student.email) == '':
                raise ContentError
            student_id = await sql_provider.set(student)
            return make_response(json.dumps(student_id), 201)
        else:
            students = []
            for student in data['students']:
                students.append(Student(surname=student['surname'], name=student['name'], \
                                        patronymic=student['patronymic'],
                                        email=student['email'], group_id=student['group_id']))
            students_ids = await sql_provider.set_many(students)
            return make_response(json.dumps(students_ids), 201)
    except (KeyError, ContentError):
        return make_response('Невалидные данные для создания студента(ов)!', 400)    
    
@admin.route('/view_student/<int:student_id>', methods=['GET'])
async def view_student(student_id):
    rk = request.args.get('rk')
    if not rk:
        return make_response('Не передан тип рубежного контроля!', 400)    
    student: Student = await sql_provider.get(Student, Q(id=student_id))
    if not student:
        return make_response('Студент не найден!', 500) 
    jsonified_rk = []
    if rk and rk == 'rk1':
        rk1: RK1 = await student.rk1
        jsonified_rk = [question_to_json(question) for question in rk1]
    elif rk and rk == 'rk2':
        rk2: RK2 = await student.rk2
        jsonified_rk = [question_to_json(question) for question in rk2]
    elif rk and rk == 'test':
        test: Test = await student.test
        jsonified_rk = [question_to_json(question) for question in test]
    return make_response(json.dumps(jsonified_rk), 200)

@admin.route('/del_student/<int:student_id>', methods=['DELETE'])
async def del_student(student_id):
    id = await sql_provider.delete(Student, student_id)
    if id:
        return make_response(json.dumps(id), 200)
    else:
        return make_response('Передан неверный id студента!', 400)

@admin.route('/patch_score/<int:question_id>', methods=['POST'])
async def patch_score(question_id):
    data = await request.get_json()
    try:
        patch = {'score': int(data['question_score'])}
        rk_cls = RK1 if data['rk'] == 'rk1' \
                 else RK2 if data['rk'] == 'rk2' \
                 else Test
        id = await sql_provider.update(rk_cls, question_id, patch)
        if id:
            return make_response(json.dumps(id), 200)
        else:
            return make_response('Передан неверный id вопроса!', 400)
    except (KeyError, ValueError):
        return make_response('Невалидные данные для обновления баллов!', 400)

@admin.route('/patch_answer/<int:question_id>', methods=['POST'])
async def patch_answer(question_id):
    data = await request.get_json()
    try:
        patch = {'student_answer': data['answer']}
        rk_cls = RK1 if data['rk'] == 'rk1' \
                 else RK2 if data['rk'] == 'rk2' \
                 else Test
        id = await sql_provider.update(rk_cls, question_id, patch)
        if id:
            return make_response(json.dumps(id), 200)
        else:
            return make_response('Передан неверный id вопроса!', 400)
    except KeyError:
        return make_response('Невалидные данные для изменения ответа!', 400)

@admin.route('/patch_email/<int:student_id>', methods=['POST'])
async def patch_email(student_id):
    data = await request.get_json()
    try:
        patch = {'email': data['email']}
        id = await sql_provider.update(Student, student_id, patch)
        if id:
            return make_response(json.dumps(id), 200)
        else:
            return make_response('Передан неверный id студента!', 400)
    except KeyError:
        return make_response('Невалидные данные для обновления email!', 400)

@admin.route('/del_questions', methods=['DELETE'])
async def del_questions():
    student_id = request.args.get('student_id')
    test_name = request.args.get('test_name')
    if student_id and test_name:
        rk_cls = RK1 if test_name == 'rk1' \
                 else RK2 if test_name == 'rk2' \
                 else Test
        questions = await sql_provider.get_all(rk_cls, Q(student_id=student_id))
        questions_ids = [question.id for question in questions]
        ids = await sql_provider.delete_many(rk_cls, questions_ids)
        if ids:
            patch = {'rk1_start_time': None} \
                     if test_name == 'rk1' \
                     else {'rk2_start_time': None} \
                     if test_name == 'rk2' \
                     else {'test_start_time': None}
            patch.update({'rk1_finish_time': None} \
                          if test_name == 'rk1' \
                          else {'rk2_finish_time': None} \
                          if test_name == 'rk2' \
                          else {'test_finish_time': None})
            await sql_provider.update(Student, student_id, patch)
            return make_response(json.dumps(ids), 200)
        else:
            return make_response('Передан неверный id студента или вопросы не существуют!', 400)
    else:
        return make_response('Переданы неверные параметры запроса!', 400)