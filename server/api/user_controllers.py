from api import api
import json
from flask import Blueprint, request, send_from_directory
from flask.helpers import make_response
from api.modules.support_utilies import load_task, finish_task, do_on_complete
from api.modules.json_utilies import question_to_json
from api.models.shemas import Student, RK1, RK2, Test
from api.modules.task_selector import select
from api import sql_provider, server_const
from api.modules.custom_exceptions import ContentError

user = Blueprint('user', __name__)

@user.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(api.config['UPLOAD_FOLDER'], filename)

@user.route('/test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['GET', 'POST'])
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
    interval = server_const['time_for_rk1'] if rk_choice == 'rk1' \
               else server_const['time_for_rk2'] if rk_choice == 'rk2' \
               else server_const['time_for_test']
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