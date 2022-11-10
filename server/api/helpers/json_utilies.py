from json import dumps
from api.models import Group, Student, Year, RK1, RK2, Test, Teacher, TestType
from transliterate import translit

async def year_to_json(year: Year):
    if year:
        year_fields = { k:v for k, v in vars(year).items() if not k.startswith('_') }
        return dumps(year_fields, ensure_ascii=False)

async def group_to_json(group: Group):
    if group:
        group_fields = { k:v for k, v in vars(group).items() if not k.startswith('_') }
        return dumps(group_fields, ensure_ascii=False) 
    
async def student_to_json(student: Student):
    if student:
        student_fields = { k:v for k, v in vars(student).items() if not k.startswith('_') }
        student_fields['rk1_score'] = await student.rk1_score
        student_fields['rk2_score'] = await student.rk2_score
        student_fields['test_score'] = await student.test_score
        return dumps(student_fields, ensure_ascii=False)

async def question_to_json(question: RK1 or RK2 or Test):
    if question:
        question_fields = { k:v for k, v in vars(question).items() if not k.startswith('_') }
        return dumps(question_fields, ensure_ascii=False)

async def teacher_to_json(teacher: Teacher):
    if teacher:
        teacher_fields = { k:v for k, v in vars(teacher).items() if not k.startswith('_') }
        teacher_fields["teacher_view"] = teacher.teacher_name
        teacher_fields["teacher_name"] = translit(teacher.teacher_name, reversed=True).split(' ')[0].lower()
        return dumps(teacher_fields, ensure_ascii=False)

async def test_type_to_json(test: TestType):
    if test:
        test_fields = { k:v for k, v in vars(test).items() if not k.startswith('_') }
        test_fields["test_view"] = test.test_name
        test_fields["test_name"] = translit(test.test_name, reversed=True).replace('№', '').lower()
        return dumps(test_fields, ensure_ascii=False)
