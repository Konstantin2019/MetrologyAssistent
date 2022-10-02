from api import api
import json
from flask import Blueprint, request
from flask.helpers import make_response
from datetime import datetime
from api.modules.json_utilies import year_to_json, group_to_json, student_to_json, question_to_json
from api.models.shemas import Group, Student, Year, RK1, RK2, Test
from api import sql_provider, glob
from api.modules.custom_exceptions import ContentError

admin = Blueprint('admin', __name__)

@admin.before_request
def admin_middleware():
    if glob['admin_status']:
        return None
    return make_response('Не авторизован!', 401)

@admin.route('/', methods=['GET'])
def admin_index():
    years = sql_provider.get_all(Year)
    groups = sql_provider.get_all(Group)
    students = sql_provider.get_all(Student)
    jsonfied_years = [year_to_json(year) for year in years]
    jsonfied_groups = [group_to_json(group) for group in groups]
    jsonfied_students = [student_to_json(student) for student in students]
    response = make_response(json.dumps({'years': jsonfied_years, 
                                         'groups': jsonfied_groups, 
                                         'students': jsonfied_students}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response           
    
@admin.route('/create_group', methods=['POST'])
def create_group():
    data = request.get_json()
    try:
        if len(data['group_name']) > 0:
            current_year = datetime.now().year
            year_record = sql_provider.query(Year).filter_by(year_name=current_year).scalar()
            if year_record:
                group_id = sql_provider.set(Group(group_name=data['group_name'], year_id=year_record.id))
            else:
                year = Year(year_name=current_year)
                new_year_id = sql_provider.set(year)
                group_id = sql_provider.set(Group(group_name=data['group_name'], year_id=new_year_id))
            return make_response(json.dumps(group_id), 201)
        else:
            raise ContentError
    except (KeyError, ContentError):
        return make_response('Невалидные данные для создания группы!', 400)   
    
@admin.route('/del_group/<int:group_id>', methods=['DELETE'])
def del_group(group_id):
    returned_id = sql_provider.delete(Group, group_id)
    if returned_id:
        return make_response(json.dumps(returned_id), 200)
    else:
        return make_response('Передан неверный id группы!', 400)

@admin.route('/add_students', methods=['POST'])
def add_students():
    data = request.get_json()
    try:
        if type(data) is not list:
            student = Student(surname=data['surname'], name=data['name'], patronymic=data['patronymic'],\
                              email=data['email'], group_id=data['group_id'])
            if (student.surname or student.name or student.email) == '':
                raise ContentError
            student_id = sql_provider.set(student)
            return make_response(json.dumps(student_id), 201)
        else:
            students = []
            for item in data:
                students.append(Student(surname=item['surname'], name=item['name'], patronymic=item['patronymic'], \
                                        email=item['email'], group_id=item['group_id']))
            students_ids = sql_provider.set_many(students)
            return make_response(json.dumps(students_ids), 201)
    except (KeyError, ContentError):
        return make_response('Невалидные данные для создания студента(ов)!', 400)    
    
@admin.route('/view_student/<int:student_id>', methods=['GET'])
def view_student(student_id):
    rk = request.args.get('rk')
    if not rk:
        return make_response('Не передан тип рубежного контроля!', 400)    
    student = sql_provider.get(Student, student_id)
    if not student:
        return make_response('Студент не найден!', 500) 
    jsonified_rk = []
    if rk and rk == 'rk1':
        rk1 = student.rk1_questions
        jsonified_rk = [question_to_json(question) for question in rk1]
    elif rk and rk == 'rk2':
        rk2 = student.rk2_questions
        jsonified_rk = [question_to_json(question) for question in rk2]
    elif rk and rk == 'test':
        test = student.test_questions
        jsonified_rk = [question_to_json(question) for question in test]
    return make_response(json.dumps(jsonified_rk), 200)

@admin.route('/del_student/<int:student_id>', methods=['DELETE'])
def del_student(student_id):
    returned_id = sql_provider.delete(Student, student_id)
    if returned_id:
        return make_response(json.dumps(returned_id), 200)
    else:
        return make_response('Передан неверный id студента!', 400)

@admin.route('/patch_score/<int:question_id>', methods=['POST'])
def patch_score(question_id):
    data = request.get_json()
    try:
        patch = {'score': int(data['question_score'])}
        rk_cls = RK1 if data['rk'] == 'rk1' \
                 else RK2 if data['rk'] == 'rk2' \
                 else Test
        returned_id = sql_provider.update(rk_cls, question_id, patch)
        if returned_id:
            return make_response(json.dumps(returned_id), 200)
        else:
            return make_response('Передан неверный id вопроса!', 400)
    except (KeyError, ValueError):
        return make_response('Невалидные данные для обновления баллов!', 400)

@admin.route('/patch_answer/<int:question_id>', methods=['POST'])
def patch_answer(question_id):
    data = request.get_json()
    try:
        patch = {'student_answer': data['answer']}
        rk_cls = RK1 if data['rk'] == 'rk1' \
                 else RK2 if data['rk'] == 'rk2' \
                 else Test
        returned_id = sql_provider.update(rk_cls, question_id, patch)
        if returned_id:
            return make_response(json.dumps(returned_id), 200)
        else:
            return make_response('Передан неверный id вопроса!', 400)
    except (KeyError, ValueError):
        return make_response('Невалидные данные для изменения ответа!', 400)

@admin.route('/patch_email/<int:student_id>', methods=['POST'])
def patch_email(student_id):
    data = request.get_json()
    try:
        patch = {'email': data['email']}
        returned_id = sql_provider.update(Student, student_id, patch)
        if returned_id:
            return make_response(json.dumps(returned_id), 200)
        else:
            return make_response('Передан неверный id студента!', 400)
    except:
        return make_response('Невалидные данные для обновления email!', 400)

@admin.route('/del_questions', methods=['POST'])
def del_questions():
    data = request.get_json()
    try:
        student_id = data['student_id']
        test_name = data['test_name']
        rk_cls = RK1 if test_name == 'rk1' \
                 else RK2 if test_name == 'rk2' \
                 else Test
        questions = sql_provider.query(rk_cls).filter_by(student_id=student_id).all()
        questions_ids = [question.id for question in questions]
        returned_ids = sql_provider.delete_many(rk_cls, questions_ids)
        if returned_ids:
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
            sql_provider.update(Student, student_id, patch)
            return make_response(json.dumps(returned_ids), 200)
        else:
            return make_response('Передан неверный id студента или вопросы не существуют!', 400)
    except KeyError:
        return make_response('Переданы неверные параметры запроса!', 400)