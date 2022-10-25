from api import api, sql_provider, dteachers
from datetime import datetime
from random import randint
from api.models import Student, RK1, RK2, Test
from api.modules.custom_exceptions import ContentError
from api.modules.task_selector import select

async def prelude(student_id: int, rk_choice: str, teacher: str, post=False):
    student = await sql_provider.get(Student, key={'id': student_id})
    if not student:
        return 404
    start_time = student.rk1_start_time if rk_choice == 'rk1' \
                 else student.rk2_start_time if rk_choice == 'rk2' \
                 else student.test_start_time
    finish_time = student.rk1_finish_time if rk_choice == 'rk1' \
                  else student.rk2_finish_time if rk_choice == 'rk2' \
                  else student.test_finish_time
    if finish_time:
        return 400
    interval = dteachers[teacher].rk1_time if rk_choice == 'rk1' \
               else dteachers[teacher].rk2_time if rk_choice == 'rk2' \
               else dteachers[teacher].test_time
    checker, task1_loader, task2_loader, test_loader = select(teacher)
    rk_loader = task1_loader if rk_choice == 'rk1' \
                else task2_loader if rk_choice == 'rk2' \
                else test_loader
    rk_cls = RK1 if rk_choice == 'rk1' \
             else RK2 if rk_choice == 'rk2' \
             else Test
    if post:
        return checker, rk_cls
    return student, start_time, finish_time, interval, rk_loader, rk_cls

async def load_task(student, teacher, rk_choice, rk_loader, rk_cls, start_time=None, finish_time=None):
    file_name = 'rk1.json' if rk_choice == 'rk1' \
                else 'rk2.json' if rk_choice == 'rk2' \
                else 'test.json'
    if finish_time:
        return []
    if not start_time:
        try:
            rk_path = api.config['UPLOAD_FOLDER'] + f'/{teacher}/task_template/{file_name}'
            rk: dict = await rk_loader.load_tasks_async(rk_path)
            questions = [rk_cls(index=i+1, question=text, correct_answer=answer, \
                                student=student, score=0, \
                                image_url=f'/api/user/download/{teacher}/images/{rk_choice}/{i+1}.jpg')
                         for i, (text, answer) in enumerate(rk.items())]
            questions = await sql_provider.set_many(questions)
            time_patch = {'rk1_start_time': datetime.now().isoformat()} if rk_choice == 'rk1' \
                         else {'rk2_start_time': datetime.now().isoformat()} if rk_choice == 'rk2' \
                         else {'test_start_time': datetime.now().isoformat()}
            await sql_provider.update(Student, student.id, time_patch)
            start_time = time_patch['rk1_start_time'] if rk_choice == 'rk1' \
                         else time_patch['rk2_start_time'] if rk_choice == 'rk2' \
                         else time_patch['test_start_time']
        except:
            return None, None
    else:
        questions = await sql_provider.get_all(rk_cls, filter={'student_id': student.id})
    return start_time, questions

async def finish_task(question_id, question_index, student_answer, checker, rk_choice, rk_cls):
    try:
        index = int(question_index)
        question = await sql_provider.get(rk_cls, key={'id': question_id})
        if not question:
            raise ContentError
        correct_answer = question.correct_answer
        score, answer = checker.RK1_Checker(correct_answer, student_answer)(index) if rk_choice == 'rk1' \
                        else checker.RK2_Checker(correct_answer, student_answer)(index) if  rk_choice == 'rk2' \
                        else checker.Test_Checker(correct_answer, student_answer)(index)
        await sql_provider.update(rk_cls, question_id, {'student_answer': answer, 'score': score})
        return question_id
    except (ValueError, ContentError):
        return None

async def do_on_complete(student_id, test_name):
    patch = {'rk1_finish_time': datetime.now().isoformat()} if test_name == 'rk1' \
            else {'rk2_finish_time': datetime.now().isoformat()} if test_name == 'rk2' \
            else {'test_finish_time': datetime.now().isoformat()}
    await sql_provider.update(Student, student_id, patch)

def generate_token():
    rand = [chr(randint(97, 122)) for i in range(20)]
    return ''.join(rand)