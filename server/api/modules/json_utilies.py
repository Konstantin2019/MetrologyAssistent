from flask import jsonify
from api.models.shemas import Group, Student, Year, RK1, RK2, Test, Teacher, TestType
from transliterate import translit

def year_to_json(year: Year):
    return jsonify(id=year.id, year_name=year.year_name) \
                   .data.decode('utf-8')

def group_to_json(group: Group):
    return jsonify(id=group.id, group_name=group.group_name, year_id=group.year_id) \
                   .data.decode('utf-8')
    
def student_to_json(student: Student):
    return jsonify(id=student.id, surname=student.surname, name=student.name, \
                   patronymic=student.patronymic, email=student.email, \
                   rk1_score=student.rk1_score, rk2_score=student.rk2_score, \
                   test_score=student.test_score, group_id=student.group_id) \
                   .data.decode('utf-8')

def question_to_json(question: RK1 or RK2 or Test):
    return jsonify(id=question.id, index=question.index, question=question.question, \
                   student_answer=question.student_answer, \
                   correct_answer=question.correct_answer, \
                   score=question.score, image_url=question.image_url,\
                   student_id=question.student_id) \
                   .data.decode('utf-8')

def teacher_to_json(teacher: Teacher):
    return jsonify(id=teacher.id, teacher_view=teacher.teacher_name, \
                   teacher_name=translit(teacher.teacher_name, reversed=True)\
                   .split(' ')[0].lower()) \
                   .data.decode('utf-8')

def test_type_to_json(test: TestType):
    return jsonify(id=test.id, test_view=test.test_name, \
                   test_name=translit(test.test_name, reversed=True)
                   .replace('№', '').lower() ) \
                   .data.decode('utf-8')