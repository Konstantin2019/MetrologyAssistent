from tortoise.models import Model
from tortoise import fields

class Year(Model):
    id = fields.UUIDField(pk=True)
    year_name = fields.IntField()

    def __str__(self):
        return self.year_name

    class Meta():
        table = 'years'

class Group(Model):
    id = fields.UUIDField(pk=True)
    group_name = fields.CharField(max_length=12)
    year_id = fields.ForeignKeyField('models.Year', related_name='groups', on_delete=fields.CASCADE)

    def __str__(self):
        return self.group_name
    
    class Meta():
        table = 'student_groups'

class Student(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=32)
    surname = fields.CharField(max_length=32)
    patronymic = fields.CharField(max_length=32, null=True)
    email = fields.CharField(max_length=64)
    group_id = fields.ForeignKeyField('models.Group', related_name='students', on_delete=fields.CASCADE)
    rk1_start_time = fields.CharField(max_length=64, null=True)
    rk1_finish_time = fields.CharField(max_length=64, null=True)
    __rk1 = []
    rk2_start_time = fields.CharField(max_length=64, null=True)
    rk2_finish_time = fields.CharField(max_length=64, null=True)
    __rk2 = []
    test_start_time = fields.CharField(max_length=64, null=True)
    test_finish_time = fields.CharField(max_length=64, null=True)
    __test = []
    __rk1_score = fields.IntField(null=True)
    __rk2_score = fields.IntField(null=True)
    __test_score = fields.IntField(null=True)

    @property
    async def rk1(self):
        self.__rk1 = await self.fetch_related('rk1_questions')
        return self.__rk1

    @property
    async def rk2(self):
        self.__rk2 = await self.fetch_related('rk2_questions')
        return self.__rk2

    @property
    async def test(self):
        self.__test = await self.fetch_related('test_questions')
        return self.__test

    @property
    def rk1_score(self):
        self.__rk1_score = sum(self.__rk1)
        return self.__rk1_score

    @property
    def rk2_score(self):
        self.__rk2_score = sum(self.__rk2)
        return self.__rk2_score

    @property
    def test_score(self):
        self.__test_score = sum(self.__test_score)
        return self.__test_score

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
    
    class Meta():
        table = 'students'

class RK1(Model):
    id = fields.UUIDField(pk=True)
    index = fields.IntField(null=True)
    question = fields.TextField(null=True)
    student_answer = fields.TextField(null=True)
    correct_answer = fields.TextField(null=True)
    score = fields.IntField(null=True)
    image_url = fields.CharField(max_length=64, null=True)
    student_id = fields.ForeignKeyField('models.Student', related_name='rk1_questions', on_delete=fields.CASCADE)

    def __str__(self):
        return f'question: {self.question}, correct_answer: {self.correct_answer}'
    
    class Meta():
        table = 'rk1'

class RK2(Model):
    id = fields.UUIDField(pk=True)
    index = fields.IntField(null=True)
    question = fields.TextField(null=True)
    student_answer = fields.TextField(null=True)
    correct_answer = fields.TextField(null=True)
    score = fields.IntField(null=True)
    image_url = fields.CharField(max_length=64, null=True)
    student_id = fields.ForeignKeyField('models.Student', related_name='rk2_questions', on_delete=fields.CASCADE)

    def __str__(self):
        return f'question: {self.question}, correct_answer: {self.correct_answer}'
    
    class Meta():
        table = 'rk2'

class Test(Model):
    id = fields.UUIDField(pk=True)
    index = fields.IntField(null=True)
    question = fields.TextField(null=True)
    student_answer = fields.TextField(null=True)
    correct_answer = fields.TextField(null=True)
    score = fields.IntField(null=True)
    image_url = fields.CharField(max_length=64, null=True)
    student_id = fields.ForeignKeyField('models.Student', related_name='test_questions', on_delete=fields.CASCADE)

    def __str__(self):
        return f'question: {self.question}, correct_answer: {self.correct_answer}'
    
    class Meta():
        table = 'tests'

class Teacher(Model):
    id = fields.UUIDField(pk=True)
    teacher_name = fields.CharField(max_length=32)

    def __str__(self):
        return self.teacher_name

    class Meta():
        table = 'teachers'

class TestType(Model):
    id = fields.UUIDField(pk=True)
    test_name = fields.CharField(max_length=16)

    def __str__(self):
        return self.test_name

    class Meta():
        table = 'test_types'

class Admin(Model):
    id = fields.UUIDField(pk=True)
    token = fields.TextField()

    class Meta():
        table = 'admin'
