from random import randint
from transliterate import translit
from datetime import datetime

def generate_token():
    rand = [chr(randint(97, 122)) for i in range(20)]
    return ''.join(rand) + '|' + datetime.now().isoformat()

def validate_token(token: str):
    idx = token.find('|')
    if idx > 0:
        expire = token.split('|')[1]
        timestamp = datetime.fromisoformat(expire)
        time_left = datetime.now() - timestamp
        if time_left.seconds < 3600:
            return True
    return False 

def teacher_to_eng(teacher_name: str):
    return translit(teacher_name, reversed=True).split(' ')[0].lower()

def teacher_to_ru(teacher_name: str):
    surname = translit(teacher_name, 'ru')
    if surname == "Потапов".lower():
        return "Потапов К.Г."
    elif surname == "Тумакова".lower():
        return "Тумакова Е.В."

def test_to_eng(test_name: str):
    return translit(test_name, reversed=True).replace('№', '').lower()