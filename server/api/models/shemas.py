from sqlalchemy.util.langhelpers import hybridproperty
from api import db
from sqlalchemy.orm import backref, synonym
from sqlalchemy.ext.hybrid import hybrid_property

class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    year_name = db.Column(db.Integer, nullable=False)
    unique = synonym('year_name')
    groups = db.relationship('Group', backref='year', lazy=True, cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'<year {self.year_name}>'

class Group(db.Model):
    __tablename__ = 'student_groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(12), nullable=False)
    unique = synonym('group_name')
    year_id = db.Column(db.Integer, db.ForeignKey('years.id', ondelete='CASCADE'), nullable=False)
    students = db.relationship('Student', backref='group', lazy=True, cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'<group {self.group_name}>' 

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(32), nullable=False)
    unique = synonym('email')
    name = db.Column(db.String(32), nullable=False)
    patronymic = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('student_groups.id', ondelete='CASCADE'), nullable=False)
    rk1_questions = db.relationship('RK1', backref='student', lazy=True, cascade="all, delete", passive_deletes=True)
    rk1_start_time = db.Column(db.String(32), nullable=True)
    rk1_finish_time = db.Column(db.String(32), nullable=True)
    rk2_questions = db.relationship('RK2', backref='student', lazy=True, cascade="all, delete", passive_deletes=True)
    rk2_start_time = db.Column(db.String(32), nullable=True)
    rk2_finish_time = db.Column(db.String(32), nullable=True)
    test_questions = db.relationship('Test', backref='student', lazy=True, cascade="all, delete", passive_deletes=True)
    test_start_time = db.Column(db.String(32), nullable=True)
    test_finish_time = db.Column(db.String(32), nullable=True)

    @hybrid_property
    def rk1_score(self):
        return sum(rk1_question.score for rk1_question in self.rk1_questions)

    @hybrid_property
    def rk2_score(self):
        return sum(rk2_question.score for rk2_question in self.rk2_questions)

    @hybrid_property
    def test_score(self):
        return sum(test_question.score for test_question in self.test_questions)

    def __repr__(self):
        return f'<surname {self.surname}>' 

class RK1(db.Model):
    __tablename__ = 'rk1'
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=True)
    unique = synonym('question')
    student_answer = db.Column(db.Text, nullable=True)
    correct_answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<question : {self.question}, correct_answer : {self.correct_answer}>'

class RK2(db.Model):
    __tablename__ = 'rk2'
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=True)
    unique = synonym('question')
    student_answer = db.Column(db.Text, nullable=True)
    correct_answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<question : {self.question}, correct_answer : {self.correct_answer}>'

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=True)
    unique = synonym('question')
    student_answer = db.Column(db.Text, nullable=True)
    correct_answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<question : {self.question}, correct_answer : {self.correct_answer}>'

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.Text, nullable=True)
    unique = synonym('teacher_name')

class TestType(db.Model):
    __tablename__ = 'testType'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.Text, nullable=True)
    unique = synonym('test_name')

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=True)
    unique = synonym('token')