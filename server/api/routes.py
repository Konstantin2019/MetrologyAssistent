from hashlib import sha1
import json
from flask import jsonify, request, send_from_directory, session
from flask.helpers import make_response
from datetime import datetime
from api.modules.sheduler import do_on_complete
from api.modules.json_utilies import year_to_json, group_to_json, student_to_json, question_to_json
from api.models.shemas import Group, Student, Year, RK1, RK2, Test
from api import sql_provider, store
from api.modules.task_selector import select
from api.modules.custom_exceptions import ContentError

def init_controllers(api):

    #region Admin
    def auth_middleware():
        admin_login = request.cookies.get('admin_login')
        admin_password = request.cookies.get('admin_password')
        if not admin_login and not admin_password:
            return False
        correct_hash_code = sha1(str.encode(api.config['ADMIN_PASSWORD'])).hexdigest()
        if admin_login != api.config['ADMIN_LOGIN'] and admin_password != correct_hash_code:
            return False
        return True

    @api.route('/api/admin_auth', methods=['POST'])
    def admin_auth():
        credentials = request.get_json()
        try:
            input_hash_code = sha1(str.encode(credentials['password'])).hexdigest()
            correct_hash_code = sha1(str.encode(api.config['ADMIN_PASSWORD'])).hexdigest() 
            if credentials['login'] == api.config['ADMIN_LOGIN'] and input_hash_code == correct_hash_code:
                admin_login = request.cookies.get('admin_login')
                admin_password = request.cookies.get('admin_password')
                if admin_login and admin_password:
                    return make_response('ОК', 200)
                else:
                    response = make_response('ОК', 200)
                    response.set_cookie('admin_login', credentials['login'])
                    response.set_cookie('admin_password', correct_hash_code)
                    return response
            else:
                return make_response('Неверная пара логин/пароль!', 401)
        except (TypeError, KeyError):
            return make_response('', 400)  

    @api.route('/api/admin', methods=['GET'])
    def admin_index():
        success = auth_middleware()
        if success:
            years = sql_provider.get_all(Year)
            groups = sql_provider.get_all(Group)
            students = sql_provider.get_all(Student)
            jsonfied_years = [year_to_json(year) for year in years]
            jsonfied_groups = [group_to_json(group) for group in groups]
            jsonfied_students = [student_to_json(student) for student in students]
            return make_response(json.dumps({'years': jsonfied_years, 
                                             'groups': jsonfied_groups, 
                                             'students': jsonfied_students}), 200)
        else:
            return make_response('Не удалось авторизоваться!', 401)
    
    @api.route('/api/admin/create_group', methods=['POST'])
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
    
    @api.route('/api/admin/del_group/<int:group_id>', methods=['DELETE'])
    def del_group(group_id):
        returned_id = sql_provider.delete(Group, group_id)
        if returned_id:
            return make_response(json.dumps(returned_id), 200)
        else:
            return make_response('Передан неверный id группы!', 400)

    @api.route('/api/admin/add_students', methods=['POST'])
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
    
    @api.route('/api/admin/view_student/<int:student_id>', methods=['GET'])
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

    @api.route('/api/admin/del_student/<int:student_id>', methods=['DELETE'])
    def del_student(student_id):
        returned_id = sql_provider.delete(Student, student_id)
        if returned_id:
            return make_response(json.dumps(returned_id), 200)
        else:
            return make_response('Передан неверный id студента!', 400)

    @api.route('/api/admin/patch_score/<int:question_id>', methods=['POST'])
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

    @api.route('/api/admin/patch_answer/<int:question_id>', methods=['POST'])
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

    @api.route('/api/admin/patch_email/<int:student_id>', methods=['POST'])
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

    @api.route('/api/admin/del_questions', methods=['POST'])
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
    #endregion 

    #region Student
    @api.route('/api/download/<path:filename>', methods=['GET'])
    def download(filename):
        return send_from_directory(api.config['UPLOAD_FOLDER'], filename)

    @api.route('/api/for_auth', methods=['GET'])
    def for_auth():
        current_year = datetime.now().year
        year = sql_provider.query(Year).filter_by(year_name=current_year).scalar()
        groups = sql_provider.get_all(Group)
        if year and len(groups) > 0:
            jsonified_year = year_to_json(year)
            jsonified_groups = [group_to_json(group) for group in groups]
            session['auth_success'] = True
            return make_response(json.dumps({'year': jsonified_year, 
                                             'groups': jsonified_groups}), 200)
        else:
            session['auth_success'] = False
            return make_response('Отсутствуют учебные группы!', 500)

    @api.route('/api/user_auth', methods=['POST'])
    def user_auth():
        if not session['auth_success']:
            return make_response('Аутентификация невозможна!', 500)
        data = request.get_json()
        if 'email' in data and data['email']:
            email = data['email'].lower()
            student = sql_provider.query(Student).filter_by(email=email).scalar()
            if student:
                return make_response(json.dumps(student.id), 200)
        return make_response('Студент не найден!', 404)

    @api.route('/api/user_test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['GET', 'POST'])
    def test(student_id: int, rk_choice: str, teacher: str):
        student = sql_provider.get(Student, student_id)
        if not student:
            return make_response('Студент не найден!', 404)
        start_time = student.rk1_start_time if rk_choice == 'rk1' \
                     else student.rk2_start_time if rk_choice == 'rk2' \
                     else student.test_start_time
        finish_time = student.rk1_finish_time if rk_choice == 'rk1' \
                      else student.rk2_finish_time if rk_choice == 'rk2' \
                      else student.test_finish_time
        if finish_time:
            return make_response('Рубежный контроль уже выполнен!', 500)
        interval = store['time_for_rk1'] if rk_choice == 'rk1' \
                   else store['time_for_rk2'] if rk_choice == 'rk2' \
                   else store['time_for_test']
        checker, task1_loader, task2_loader, test_loader = select(teacher)
        rk_loader = task1_loader if rk_choice == 'rk1' \
                    else task2_loader if rk_choice == 'rk2' \
                    else test_loader
        rk_cls = RK1 if rk_choice == 'rk1' \
                 else RK2 if rk_choice == 'rk2' \
                 else Test
        if request.method == 'GET':
            start_time, questions = load_task(student, teacher, rk_choice, rk_loader, rk_cls, start_time, finish_time)
            if not start_time and not questions:
                return make_response('Ошибка загрузки вопросов', 500)
            else:
                jsonified_questions = [question_to_json(question) for question in questions] 
                return make_response(json.dumps({'start': start_time, 
                                                 'duration': interval, 
                                                 'questions': jsonified_questions}), 200)
        if request.method == 'POST':
            data = request.get_json()
            try:
                if 'status' in data and data['status'] == 'finish':
                    do_on_complete(student_id, rk_choice)
                    return make_response('', 200)
                question_id = data['question_id']
                question_index = data['index']
                student_answer = data['student_answer']
                success = finish_task(question_id, question_index, student_answer, checker, rk_choice, rk_cls)
                if not success:
                    raise ContentError
                return make_response('Ответ принят!', 200)
            except (KeyError, ContentError):
                return make_response('Ответ не валиден!', 400)

    #region task_funcs
    def load_task(student, teacher, rk_choice, rk_loader, rk_cls, start_time=None, finish_time=None):
        file_name = 'rk1.json' if rk_choice == 'rk1' \
                    else 'rk2.json' if rk_choice == 'rk2' \
                    else 'test.json'
        if finish_time:
            return []
        if not start_time:
            try:
                rk_path = api.config['UPLOAD_FOLDER'] + f'/{teacher}/task_template/{file_name}'
                rk = rk_loader.load_tasks(rk_path)
                questions = [rk_cls(index=i+1, question=text, correct_answer=answer, \
                                    student_id=student.id, score=0, \
                                    image_url=f'/api/download/{teacher}/images/{rk_choice}/{i+1}.jpg')
                             for i, (text, answer) in enumerate(rk.items())]
                sql_provider.set_many(questions)
                time_patch = {'rk1_start_time': datetime.now().isoformat()} if rk_choice == 'rk1' \
                             else {'rk2_start_time': datetime.now().isoformat()} if rk_choice == 'rk2' \
                             else {'test_start_time': datetime.now().isoformat()}
                sql_provider.update(Student, student.id, time_patch)
                start_time = time_patch['rk1_start_time'] if rk_choice == 'rk1' \
                             else time_patch['rk2_start_time'] if rk_choice == 'rk2' \
                             else time_patch['test_start_time']
            except:
                return None, None
        else:
            questions = sql_provider.query(rk_cls).filter_by(student_id=student.id).all()
        return start_time, questions

    def finish_task(question_id, question_index, student_answer, checker, rk_choice, rk_cls):
        try:
            index = int(question_index)
            question = sql_provider.get(rk_cls, question_id)
            if not question:
                raise ContentError
            correct_answer = question.correct_answer
            score, answer = checker.RK1_Checker(correct_answer, student_answer)(index) if rk_choice == 'rk1' \
                            else checker.RK2_Checker(correct_answer, student_answer)(index) if  rk_choice == 'rk2' \
                            else checker.Test_Checker(correct_answer, student_answer)(index)
            sql_provider.update(rk_cls, question_id, {'student_answer': answer, 'score': score})
            return question_id
        except (ValueError, ContentError):
            return None
    #endregion
        
    #endregion