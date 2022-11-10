from api import api
from api.providers.sql_provider import SQLProvider
from api.models import Student, RK1, RK2, Test, Teacher
from api.core.task_selector import select
from api.helpers.support_utilies import teacher_to_ru
from datetime import datetime
from api.errors import ContentError

async def prelude(provider: SQLProvider, student_id: int, rk_choice: str, teacher_name: str, post=False):
    student = await provider.get(Student, key={'id': student_id})
    if not student:
        return 'Студент не найден', 404
    start_time = student.rk1_start_time if rk_choice == 'rk1' \
                 else student.rk2_start_time if rk_choice == 'rk2' \
                 else student.test_start_time
    finish_time = student.rk1_finish_time if rk_choice == 'rk1' \
                  else student.rk2_finish_time if rk_choice == 'rk2' \
                  else student.test_finish_time
    if finish_time:
        return 'Рубежный контроль уже выполнен', 400
    teacher: Teacher = await provider.get(Teacher, key={"teacher_name": teacher_to_ru(teacher_name)})
    interval = teacher.rk1_time if rk_choice == 'rk1' \
               else teacher.rk2_time if rk_choice == 'rk2' \
               else teacher.test_time
    checker, task1_loader, task2_loader, test_loader = select(teacher_name)
    rk_loader = task1_loader if rk_choice == 'rk1' \
                else task2_loader if rk_choice == 'rk2' \
                else test_loader
    rk_cls = RK1 if rk_choice == 'rk1' \
             else RK2 if rk_choice == 'rk2' \
             else Test
    if post:
        modules = checker, rk_cls
        return modules, 200
    modules = student, start_time, finish_time, interval, rk_loader, rk_cls
    return modules, 200

async def load_task(provider: SQLProvider, *args):
    student, teacher_name, rk_choice, rk_loader, rk_cls, start_time, finish_time = args
    file_name = 'rk1.json' if rk_choice == 'rk1' \
                else 'rk2.json' if rk_choice == 'rk2' \
                else 'test.json'
    if finish_time:
        return []
    if not start_time:
        try:
            rk_path = api.config['UPLOAD_FOLDER'] + f'/{teacher_name}/task_template/{file_name}'
            rk: dict = await rk_loader.load_tasks_async(rk_path)
            questions = [rk_cls(index=i+1, question=text, correct_answer=answer, \
                                student=student, score=0, \
                                image_url=f'/api/user/download/{teacher_name}/images/{rk_choice}/{i+1}.jpg')
                         for i, (text, answer) in enumerate(rk.items())]
            questions = await provider.set_many(questions)
            time_patch = {'rk1_start_time': datetime.now().isoformat()} if rk_choice == 'rk1' \
                         else {'rk2_start_time': datetime.now().isoformat()} if rk_choice == 'rk2' \
                         else {'test_start_time': datetime.now().isoformat()}
            await provider.update(Student, student.id, time_patch)
            start_time = time_patch['rk1_start_time'] if rk_choice == 'rk1' \
                         else time_patch['rk2_start_time'] if rk_choice == 'rk2' \
                         else time_patch['test_start_time']
        except:
            return None, None
    else:
        questions = await provider.get_all(rk_cls, filter={'student_id': student.id})
    return start_time, questions

async def finish_task(provider: SQLProvider, *args):
    question_id, question_index, student_answer, checker, rk_choice, rk_cls = args
    try:
        index = int(question_index)
        question = await provider.get(rk_cls, key={'id': question_id})
        if not question:
            raise ContentError
        correct_answer = question.correct_answer
        score, answer = checker.RK1_Checker(correct_answer, student_answer)(index) if rk_choice == 'rk1' \
                        else checker.RK2_Checker(correct_answer, student_answer)(index) if  rk_choice == 'rk2' \
                        else checker.Test_Checker(correct_answer, student_answer)(index)
        await provider.update(rk_cls, question_id, {'student_answer': answer, 'score': score})
        return question_id
    except (ValueError, ContentError):
        return None

async def do_on_complete(provider: SQLProvider, student_id: int, test_name: str):
    patch = {'rk1_finish_time': datetime.now().isoformat()} if test_name == 'rk1' \
            else {'rk2_finish_time': datetime.now().isoformat()} if test_name == 'rk2' \
            else {'test_finish_time': datetime.now().isoformat()}
    await provider.update(Student, student_id, patch)