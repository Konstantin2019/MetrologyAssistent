from typing import List
from tortoise.models import Model
from tortoise import fields

class Year(Model):
    id = fields.IntField(pk=True)
    year_name = fields.IntField()

    def __str__(self):
        return self.year_name

    class Meta():
        table = 'years'

class Group(Model):
    id = fields.IntField(pk=True)
    group_name = fields.CharField(max_length=12)
    year = fields.ForeignKeyField('models.Year', related_name='groups', on_delete=fields.CASCADE)

    def __str__(self):
        return self.group_name
    
    class Meta():
        table = 'student_groups'

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32)
    surname = fields.CharField(max_length=32)
    patronymic = fields.CharField(max_length=32, null=True)
    email = fields.CharField(max_length=64)
    group = fields.ForeignKeyField('models.Group', related_name='students', on_delete=fields.CASCADE)
    rk1_start_time = fields.CharField(max_length=64, null=True)
    rk1_finish_time = fields.CharField(max_length=64, null=True)
    rk2_start_time = fields.CharField(max_length=64, null=True)
    rk2_finish_time = fields.CharField(max_length=64, null=True)
    test_start_time = fields.CharField(max_length=64, null=True)
    test_finish_time = fields.CharField(max_length=64, null=True)
    __rk1_score = 0
    __rk2_score = 0
    __test_score = 0

    async def rk1(self):
        await self.fetch_related('rk1_questions')
        return list(self.rk1_questions)

    async def rk2(self):
        await self.fetch_related('rk2_questions')
        return list(self.rk2_questions)

    async def test(self):
        await self.fetch_related('test_questions')
        return list(self.test_questions)

    @property
    async def rk1_score(self):
        qs: List[RK1] = await self.rk1()
        self.__rk1_score = sum([q.score for q in qs])
        return self.__rk1_score

    @property
    async def rk2_score(self):
        qs: List[RK2] = await self.rk2()
        self.__rk2_score = sum([q.score for q in qs])
        return self.__rk2_score

    @property
    async def test_score(self):
        qs: List[Test] = await self.test()
        self.__test_score = sum([q.score for q in qs])
        return self.__test_score

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
    
    class Meta():
        table = 'students'

class RK1(Model):
    id = fields.IntField(pk=True)
    index = fields.IntField(null=True)
    question = fields.TextField(null=True)
    student_answer = fields.TextField(null=True)
    correct_answer = fields.TextField(null=True)
    score = fields.IntField(null=True)
    answer_screen = fields.BinaryField(null=True)
    image_url = fields.CharField(max_length=64, null=True)
    student = fields.ForeignKeyField('models.Student', related_name='rk1_questions', on_delete=fields.CASCADE)

    def __str__(self):
        return f'question: {self.question}, correct_answer: {self.correct_answer}'
    
    class Meta():
        table = 'rk1'

class RK2(Model):
    id = fields.IntField(pk=True)
    index = fields.IntField(null=True)
    question = fields.TextField(null=True)
    student_answer = fields.TextField(null=True)
    correct_answer = fields.TextField(null=True)
    score = fields.IntField(null=True)
    answer_screen = fields.BinaryField(null=True)
    image_url = fields.CharField(max_length=64, null=True)
    student = fields.ForeignKeyField('models.Student', related_name='rk2_questions', on_delete=fields.CASCADE)

    def __str__(self):
        return f'question: {self.question}, correct_answer: {self.correct_answer}'
    
    class Meta():
        table = 'rk2'

class Test(Model):
    id = fields.IntField(pk=True)
    index = fields.IntField(null=True)
    question = fields.TextField(null=True)
    student_answer = fields.TextField(null=True)
    correct_answer = fields.TextField(null=True)
    score = fields.IntField(null=True)
    answer_screen = fields.BinaryField(null=True)
    image_url = fields.CharField(max_length=64, null=True)
    student = fields.ForeignKeyField('models.Student', related_name='test_questions', on_delete=fields.CASCADE)

    def __str__(self):
        return f'question: {self.question}, correct_answer: {self.correct_answer}'
    
    class Meta():
        table = 'tests'

class Admin(Model):
    id = fields.IntField(pk=True)
    token = fields.TextField()

    class Meta():
        table = 'admin'

class Teacher(Model):
    id = fields.IntField(pk=True)
    teacher_name = fields.CharField(max_length=32)
    rk1_time = fields.IntField(null=True)
    rk2_time = fields.IntField(null=True)
    test_time = fields.IntField(null=True)

    class Meta():
        table = 'teachers'

class TestType(Model):
    id = fields.IntField(pk=True)
    test_name = fields.CharField(max_length=12)

    class Meta():
        table = 'test_types'