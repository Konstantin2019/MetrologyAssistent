from api.providers.sql_provider import SQLProvider
from api.core.core_ops import prelude, load_task, finish_task, do_on_complete
from api.helpers.json_utilies import question_to_json
from json import dumps
from api.error import ContentError

async def get_test_handler(provider: SQLProvider, student_id: int, rk_choice: str, teacher: str):
    state = await prelude(provider, student_id, rk_choice, teacher)
    if state[1] != 200:
        return state
    student, start_time, finish_time, interval, rk_loader, rk_cls = state[0] 
    start_time, questions = await load_task(provider, student, teacher, rk_choice, rk_loader, rk_cls, start_time, finish_time)
    if not start_time and not questions:
        return 'Ошибка загрузки вопросов', 500
    jsonified_questions = [await question_to_json(question) for question in questions] 
    return dumps({'start': start_time, 'duration': interval, 'questions': jsonified_questions}), 200

async def send_test_handler(provider: SQLProvider, student_id: int, rk_choice: str, teacher: str, payload: dict):
    state = await prelude(provider, student_id, rk_choice, teacher, post=True)
    if state[1] != 200:
        return await state
    checker, rk_cls = state[0] 
    try:
        if payload and 'status' in payload and payload['status'] == 'finish':
            await do_on_complete(provider, student_id, rk_choice)
            return '', 204
        question_id = payload['question_id']
        question_index = payload['index']
        student_answer = payload['student_answer']
        success = await finish_task(provider, question_id, question_index, student_answer, checker, rk_choice, rk_cls)
        if not success:
            raise ContentError
        return 'Ответ принят!', 200
    except KeyError:
        return 'Ответ не валиден!', 400
    except ContentError:
        return 'Ошибка сервера, вопрос не найден!', 500