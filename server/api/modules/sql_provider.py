from flask_sqlalchemy import SQLAlchemy
from api.models.shemas import Year, Group, Student, RK1, RK2, Test, Admin, Teacher, TestType
from os import getenv

if getenv('SQLALCHEMY_DATABASE_URI') == 'sqlite:///':
    import api.modules.sqlite_fix

class SQLInitializer():
    def __call__(self, orm_object: SQLAlchemy):
        try:
            orm_object.create_all()
            print('Инициализация базы данных успешна...')
            sql_provider = SQLProvider(orm_object)
            teacher_id = sql_provider.set_many([Teacher(teacher_name='Потапов К.Г.'), Teacher(teacher_name='Тумакова Е.В.')])
            test_type_id = sql_provider.set_many([TestType(test_name='РК№1'), TestType(test_name='РК№2'), TestType(test_name='Зачёт')])
            if not teacher_id or not test_type_id:
                raise Exception('Не удалось создать таблицы типа РК и преподавателей!')
            return SQLProvider(orm_object)
        except Exception as error:
            print(error)

class SQLProvider():
    def __init__(self, orm_object: SQLAlchemy):
        self.orm = orm_object

    def get_all(self, cls):
        return cls.query.all()

    def get(self, cls, id):
        return cls.query.get(id)

    def query(self, cls):
        return cls.query

    def set(self, obj):
        cls = obj.__class__
        try:
            record = cls.query.filter_by(unique=obj.unique).scalar()
            if not record:
                self.orm.session.add(obj)
                self.orm.session.flush()
                self.orm.session.commit()
                print(f'Запись {obj.unique} с id : {obj.id} успешно добавлена в таблицу {cls.__name__}...')
                return obj.id
            else:
                print(f'Запись {obj.unique} с id : {record.id} уже содержится в таблице {cls.__name__}...')
                return record.id
        except Exception as err:
            self.orm.session.rollback()
            print('Ошибка добавления в БД : ' + str(err))

    def set_many(self, objs: list):
        if len(objs) > 0:
            obj_ids = []
            for obj in objs:
                obj_ids.append(self.set(obj))
            return obj_ids
        else:
            raise ValueError

    def update(self, cls, id, data):
        try:
            cls.query.filter_by(id=id).update(data, synchronize_session='evaluate')
            self.orm.session.commit()
            print(f'Запись таблицы {cls.__name__} с id : {id} успешно изменена...')
            return id
        except Exception as err:
            self.orm.session.rollback()
            print('Ошибка модификации в БД : ' + str(err)) 

    def delete(self, cls, id):
        try:
            item = cls.query.filter_by(id=id).scalar()
            if item:
                self.orm.session.delete(item)
                self.orm.session.commit()
                print(f'Запись таблицы {cls.__name__} с id : {id} успешно удалена...')
                return id
            else:
                print('В БД отсутстует сущность с заданным id')
                return -1
        except Exception as err:
            self.orm.session.rollback()
            print('Ошибка удаления из БД : ' + str(err))
    
    def delete_many(self, cls, ids: list):
        if len(ids) > 0:
            for id in ids:
                self.delete(cls, id)
            return ids
        else:
            raise ValueError