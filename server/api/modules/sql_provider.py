from typing import TypeVar
from models import *
from tortoise.expressions import Q
from tortoise.exceptions import DoesNotExist, IntegrityError, TransactionManagementError, FieldError
import logging
import asyncio

Tortoise_model = TypeVar('Tortoise_model', Admin, Year, Group, Student, Teacher, TestType, RK1, RK2, Test)

class SQLProvider():
    def __init__(self):
        teachers = [Teacher(teacher_name='Потапов К.Г.'), Teacher(teacher_name='Тумакова Е.В.')]
        tests = [TestType(test_name='РК№1'), TestType(test_name='РК№2'), TestType(test_name='Зачёт')]
        loop = asyncio.get_running_loop()
        teachers_ids = asyncio.run_coroutine_threadsafe(self.set_many(teachers), loop).result()
        tests_type_ids = asyncio.run_coroutine_threadsafe(self.set_many(tests), loop).result()
        if not teachers_ids or not tests_type_ids:
            logging.error('Не удалось создать таблицы типа РК и преподавателей!')

    async def get_all(self, model: Tortoise_model, filter: Q=None):
        if not filter:
            items = await model.all()
        else:
            items = await model.filter(filter).all()
        return items

    async def get(self, model: Tortoise_model, expr: Q):
        try:
            item = await model.get(expr)
            return item
        except DoesNotExist:
            logging.info('Объект не найден!')
        except Exception as err:
            logging.error(err)

    async def set(self, instance: Tortoise_model):
        model = instance.__class__
        try:
            item, created = await model.get_or_create(instance)
            if created:
                logging.info(f'Запись в таблице {model.__name__} с id : {item.id} успешно создана!')
            else:
                logging.info(f'Запись в таблице {model.__name__} с id : {item.id} уже существует!')
            return item.id
        except IntegrityError:
            logging.error(f'Ошибка создания объекта {instance}!')
        except TransactionManagementError:
            logging.error('Ошибка транзакции!')

    async def set_many(self, instances: list):
        if len(instances) > 0:
            ids = await asyncio.gather([self.set(instance) for instance in instances])
            ids = [id for id in ids if id]
            return ids
        else:
            logging.error('Список на создание пустой!')

    async def update(self, model: Tortoise_model, id: int, data: dict):
        item = await model.filter(id=id)
        if item:
            await model.filter(id=id).update(data)
            logging.info(f'Запись в таблице {model.__name__} с id : {id} успешно изменена!')
            return id
        else:
            logging.warning(f'Запись с id: {id} не найдена!')

    async def delete(self, model: Tortoise_model, id: int):
        item = await model.filter(id=id)
        if item:
            await model.filter(id=id).delete()
            logging.info(f'Запись в таблице {model.__name__} с id : {id} успешно удалена...')
            return id
        else:
            logging.warning(f'Запись с id: {id} не найдена!')
    
    async def delete_many(self, model: Tortoise_model, ids: list):
        if len(ids) > 0:
            ids = await asyncio.gather([self.delete(model, id) for id in ids])
            return ids
        else:
            logging.error('Список на удаление пустой!')