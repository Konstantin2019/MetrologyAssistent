from api.providers.sql_provider import SQLProvider
from api.helpers.json_utilies import *
from datetime import datetime
from api.error import ContentError

async def admin_index_handler(provider: SQLProvider):
    years = await provider.get_all(Year)
    groups = await provider.get_all(Group)
    students = await provider.get_all(Student)
    tests = await provider.get_all(TestType)
    jsonfied_years = [await year_to_json(year) for year in years]
    jsonfied_groups = [await group_to_json(group) for group in groups]
    jsonfied_students = [await student_to_json(student) for student in students]
    jsonified_tests = [await test_type_to_json(test) for test in tests]
    return dumps({'years': jsonfied_years, 'groups': jsonfied_groups, \
                  'students': jsonfied_students, 'tests': jsonified_tests}), 200


async def create_group_handler(provider: SQLProvider, payload: dict):
    try:
        if len(payload['group_name']) > 0:
            current_year = datetime.now().year
            year: Year = await provider.get(Year, key={'year_name': current_year})
            if year:
                new_group = Group(group_name=payload['group_name'], year=year)
                group: Group = await provider.set(new_group)
            else:
                year = Year(year_name=current_year)
                new_year: Year = await provider.set(year)
                new_group = Group(group_name=payload['group_name'], year=new_year)
                group: Group = await provider.set(new_group)
            return dumps(group.id), 201
        else:
            raise ContentError
    except (KeyError, ContentError):
        return 'Невалидные данные для создания группы!', 400   

async def del_group_handler(provider: SQLProvider, group_id: int):
    id = await provider.delete(Group, group_id)
    if id:
        return dumps(id), 200
    else:
        return 'Передан неверный id группы!', 400

async def add_students_handler(provider: SQLProvider, payload: dict):
    try:
        if type(payload['students']) is not list:
            group: Group = await provider.get(Group, key={'id': payload['students']['group_id']})
            student = Student(surname=payload['students']['surname'], name=payload['students']['name'], \
                              patronymic=payload['students']['patronymic'],
                              email=payload['students']['email'], group=group)
            if (student.surname or student.name or student.email) == '':
                raise ContentError
            student: Student = await provider.set(student)
            return dumps(student.id), 201
        else:
            students: list[Student] = []
            for student in payload['students']:
                group: Group = await provider.get(Group, key={'id': student['group_id']})
                students.append(Student(surname=student['surname'], name=student['name'], \
                                        patronymic=student['patronymic'],
                                        email=student['email'], group=group))
            students = await provider.set_many(students)
            return dumps([student.id for student in students]), 201
    except (KeyError, ContentError):
        return 'Невалидные данные для создания студента(ов)!', 400   

async def view_student_handler(provider: SQLProvider, student_id: int, rk: str):
    if not rk:
        return 'Не передан тип рубежного контроля!', 400    
    student: Student = await provider.get(Student, key={'id': student_id})
    if not student:
        return 'Студент не найден!', 500 
    jsonified_rk = []
    if rk and rk == 'rk1':
        rk1: RK1 = await student.rk1()
        jsonified_rk = [await question_to_json(question) for question in rk1]
    elif rk and rk == 'rk2':
        rk2: RK2 = await student.rk2()
        jsonified_rk = [await question_to_json(question) for question in rk2]
    elif rk and rk == 'test':
        test: Test = await student.test()
        jsonified_rk = [await question_to_json(question) for question in test]
    return dumps(jsonified_rk), 200

async def del_student_handler(provider: SQLProvider, student_id: int):
    id = await provider.delete(Student, student_id)
    if id:
        return dumps(id), 200
    else:
        return 'Передан неверный id студента!', 400

async def patch_score_handler(provider: SQLProvider, question_id: int, payload: dict):
    try:
        patch = {'score': int(payload['question_score'])}
        rk_cls = RK1 if payload['rk'] == 'rk1' \
                 else RK2 if payload['rk'] == 'rk2' \
                 else Test
        id = await provider.update(rk_cls, question_id, patch)
        if id:
            return dumps(id), 200
        else:
            return 'Передан неверный id вопроса!', 400
    except (KeyError, ValueError):
        return 'Невалидные данные для обновления баллов!', 400

async def patch_answer_handler(provider: SQLProvider, question_id: int, payload: dict):
    try:
        patch = {'student_answer': payload['answer']}
        rk_cls = RK1 if payload['rk'] == 'rk1' \
                 else RK2 if payload['rk'] == 'rk2' \
                 else Test
        id = await provider.update(rk_cls, question_id, patch)
        if id:
            return dumps(id), 200
        else:
            return 'Передан неверный id вопроса!', 400
    except KeyError:
        return 'Невалидные данные для изменения ответа!', 400

async def patch_email_handler(provider: SQLProvider, student_id: int, payload: dict):
    try:
        patch = {'email': payload['email']}
        id = await provider.update(Student, student_id, patch)
        if id:
            return dumps(id), 200
        else:
            return 'Передан неверный id студента!', 400
    except KeyError:
        return 'Невалидные данные для обновления email!', 400

async def del_questions_handler(provider: SQLProvider, student_id: int, test_name: str):
    if student_id and test_name:
        rk_cls = RK1 if test_name == 'rk1' \
                 else RK2 if test_name == 'rk2' \
                 else Test
        questions = await provider.get_all(rk_cls, filter={'student_id': student_id})
        questions_ids = [question.id for question in questions]
        ids = await provider.delete_many(rk_cls, questions_ids)
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
            await provider.update(Student, student_id, patch)
            return dumps(ids), 200
        else:
            return 'Передан неверный id студента или вопросы не существуют!', 400
    else:
        return 'Переданы неверные параметры запроса!', 400