from api import api
import json
from quart import Blueprint, request, make_response, send_from_directory
from api.modules.support_utilies import load_task, finish_task, do_on_complete, prelude
from api.modules.json_utilies import question_to_json
from api.modules.custom_exceptions import ContentError

user = Blueprint('user', __name__)

@user.route('/download/<path:filename>', methods=['GET'])
async def download(filename):
    response = await send_from_directory(api.config['UPLOAD_FOLDER'], filename)
    return response

@user.route('/test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['GET'])
async def get_test(student_id: int, rk_choice: str, teacher: str):
    state = await prelude(student_id, rk_choice, teacher)
    if state == 404:
        return await make_response('Студент не найден', state)
    elif state == 400:
         return await make_response('Рубежный контроль уже выполнен', state)
    student, start_time, finish_time, interval, rk_loader, rk_cls = state 
    start_time, questions = await load_task(student, teacher, rk_choice, rk_loader, rk_cls, start_time, finish_time)
    if not start_time and not questions:
        return await make_response('Ошибка загрузки вопросов', 500)
    else:
        jsonified_questions = [await question_to_json(question) for question in questions] 
        return await make_response(json.dumps({'start': start_time, 
                                               'duration': interval, 
                                               'questions': jsonified_questions}), 200)

@user.route('/test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['POST'])
async def send_test(student_id: int, rk_choice: str, teacher: str):
    state = await prelude(student_id, rk_choice, teacher, post=True)
    if state == 404:
        return await make_response('Студент не найден', state)
    elif state == 400:
         return await make_response('Рубежный контроль уже выполнен', state)
    checker, rk_cls = state 
    data = await request.get_json()
    try:
        if 'status' in data and data['status'] == 'finish':
            await do_on_complete(student_id, rk_choice)
            return await make_response('', 200)
        question_id = data['question_id']
        question_index = data['index']
        student_answer = data['student_answer']
        success = await finish_task(question_id, question_index, student_answer, checker, rk_choice, rk_cls)
        if not success:
            raise ContentError
        return await make_response('Ответ принят!', 200)
    except (KeyError, ContentError):
        return await make_response('Ответ не валиден!', 400)