from typing import TypeVar
from api.models import *
from tortoise.exceptions import DoesNotExist, IntegrityError, TransactionManagementError
import logging

Tortoise_model = TypeVar('Tortoise_model', Admin, Year, Group, Student, Teacher, TestType, RK1, RK2, Test)

class SQLProvider():
    async def get_all(self, model: Tortoise_model, filter: dict=None):
        if not filter:
            items = await model.all()
        else:
            items = await model.filter(**filter).all()
        return items

    async def get(self, model: Tortoise_model, key: dict):
        try:
            item = await model.get(**key)
            return item
        except DoesNotExist:
            logging.info('Объект не найден!')
        except Exception as err:
            logging.error(err)

    async def set(self, instance: Tortoise_model):
        model = instance.__class__
        try:
            obj_fields = { k:v for k, v in vars(instance).items() if not k.startswith('_') and not k == 'id' }
            item = await self.get(model, key=obj_fields)
            if not item:
                item = await model.create(**obj_fields)
                logging.info(f'Запись в таблице {model.__name__} с id : {item.id} успешно создана!')
            else:
                logging.info(f'Запись в таблице {model.__name__} с id : {item.id} уже существует!')
            return item
        except IntegrityError:
            logging.error(f'Ошибка создания объекта {instance}!')
        except TransactionManagementError:
            logging.error('Ошибка транзакции!')

    async def set_many(self, instances: list):
        if len(instances) > 0:
            items = []
            for instance in instances:
                items.append(await self.set(instance))
            return items
        else:
            logging.error('Список на создание пустой!')

    async def update(self, model: Tortoise_model, id: int, data: dict):
        item = await model.filter(id=id)
        if item:
            await model.filter(id=id).update(**data)
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
            returned_ids = []
            for id in ids:
                returned_ids.append(await self.delete(model, id))
            return returned_ids
        else:
            logging.error('Список на удаление пустой!')