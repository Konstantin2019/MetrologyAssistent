from random import randint
from transliterate import translit

def generate_token():
    rand = [chr(randint(97, 122)) for i in range(20)]
    return ''.join(rand)

def teacher_to_eng(teacher_name: str):
    return translit(teacher_name, reversed=True).split(' ')[0].lower()

def teacher_to_ru(teacher_name: str):
    surname = translit(teacher_name, 'ru')
    if surname == "Потапов".lower():
        return "Потапов К.Г."
    elif surname == "Тумакова".lower():
        return "Тумакова Е.в."

def test_to_eng(test_name: str):
    return translit(test_name, reversed=True).replace('№', '').lower()