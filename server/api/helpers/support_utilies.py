from random import randint

def generate_token():
    rand = [chr(randint(97, 122)) for i in range(20)]
    return ''.join(rand)