from datetime import datetime
from hashlib import sha256
from api import api, sql_provider
from api.models.shemas import Student
from api.modules.custom_exceptions import ContentError

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
                                image_url=f'/api/user/download/{teacher}/images/{rk_choice}/{i+1}.jpg')
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

def do_on_complete(student_id, test_name):
    patch = {'rk1_finish_time': datetime.now().isoformat()} if test_name == 'rk1' \
            else {'rk2_finish_time': datetime.now().isoformat()} if test_name == 'rk2' \
            else {'test_finish_time': datetime.now().isoformat()}
    sql_provider.update(Student, student_id, patch)

def validate_hash(string1: str, string2: str):
    hash1 = sha256(string1.encode('utf-8')).hexdigest()
    hash2 = sha256(string2.encode('utf-8')).hexdigest()
    if hash1 == hash2:
        return hash1
    return None
