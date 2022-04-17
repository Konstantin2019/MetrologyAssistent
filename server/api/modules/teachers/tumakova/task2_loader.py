from random import randint
from math import sqrt
from json import load, dumps

#region inner_gen_funcs
def __rk2_task1_gen():
    def __inner_gen__(D, EsD, EiD, S, EsS, EiS):
        d = D - 2*S
        Esd = EsD - 2*EsS
        Eid = EiD - 2*EiS
        return {'Task': {'D': D, 'EsD': EsD, 'EiD': EiD, 'S': S, 'EsS': EsS, 'EiS': EiS}, \
                'Answer': {'d': d, 'Esd': Esd, 'Eid': Eid}}
    D = randint(20, 100)
    EsD = randint(0, 300)
    TD = randint(300, 600)
    S = randint(0,2)
    EsS = randint(-100, 100)
    TS = randint(30, 90)
    return __inner_gen__(D=D, EsD=EsD, EiD=EsD-TD, S=S, EsS=EsS, EiS=EsS-TS)

def __rk2_task2_gen():
    def __inner_gen__(A1, A2, A3, EsS, EiS, EsA1, EiA1, EsA2, EiA2, EsA3, EiA3):
        A4 = A1 + A2 - A3
        TS = EsS - EiS
        TA1 = EsA1 - EiA1
        TA2 = EsA2 - EiA2
        TA3 = EsA3 - EiA3
        TA4 = sqrt(TS**2 - TA1**2 - TA2**2 - TA3**2)
        EmA4 = (EsA1 + EiA1)/2 + (EsA2 + EiA2)/2 + (EsS + EiS)/2 - (EsA3 + EiA3)/2
        EsA4 = round(EmA4 + TA4/2)
        EiA4 = round(EmA4 - TA4/2)
        return {'Task': {'A1': A1, 'A2': A2, 'A3': A3, \
                         'EsS': EsS, 'EiS': EiS, 'EsA1': EsA1, 'EiA1': EiA1,\
                         'EsA2': EsA2, 'EiA2': EiA2, 'EsA3': EsA3, 'EiA3': EiA3}, \
                'Answer': {'A4': A4, 'EsA4': EsA4, 'EiA4': EiA4}}
    A1 = randint(40, 80)
    A2 = randint(40, 80)
    A3 = randint(30, 70)
    EsS = randint(500, 900)
    EiS = randint(100, 400)
    EsA1 = randint(50, 100)
    EiA1 = randint(0, 50)
    EsA2 = randint(50, 100)
    EiA2 = randint(0, 50)
    EsA3 = randint(50, 100)
    EiA3 = randint(0, 50)
    return __inner_gen__(A1=A1, A2=A2, A3=A3, EsS=EsS, EiS=EiS, EsA1=EsA1, EiA1=EiA1, \
                         EsA2=EsA2, EiA2=EiA2, EsA3=EsA3, EiA3=EiA3)
    
def __rk2_task3_gen():
    def __inner_gen__(TR2, TR3, TR4):
        TR1 = TR2 + TR3 + TR4
        TR1v = round(sqrt(TR2**2 + TR3**2 + TR4**2))
        return {'Task': {'TR2': TR2, 'TR3': TR3, 'TR4': TR4}, \
                'Answer': {'TR1': TR1, 'TR1v': TR1v}}
    return __inner_gen__(TR2=randint(20, 100), TR3=randint(20, 100), TR4=randint(20, 100))
#endregion

#region inner_prepare_funcs
def __rk2_task1_prepare(text, values):
    text = text.replace('{D = }', 'D = ' + str(values['Task']['D'])) \
               .replace('{S = }', 'S = ' + str(values['Task']['S'])) \
               .replace('{EsD = }', 'EsD = ' + str(values['Task']['EsD'])) \
               .replace('{EiD = }', 'EiD = ' + str(values['Task']['EiD'])) \
               .replace('{EsS = }', 'EsS = ' + str(values['Task']['EsS'])) \
               .replace('{EiS = }', 'EiS = ' + str(values['Task']['EiS']))
    answer = { 'd': values['Answer']['d'], 'Esd': values['Answer']['Esd'], 'Eid': values['Answer']['Eid'] }
    return { text : dumps(answer) }
    
def __rk2_task2_prepare(text, values):
    text = text.replace('{A1 = }', 'A1 = ' + str(values['Task']['A1'])) \
               .replace('{A2 = }', 'A2 = ' + str(values['Task']['A2'])) \
               .replace('{A3 = }', 'A3 = ' + str(values['Task']['A3'])) \
               .replace('{Smax = }', 'Smax = ' + str(round(values['Task']['EsS']/1000, 3))) \
               .replace('{Smin = }', 'Smin = ' + str(round(values['Task']['EiS']/1000, 3))) \
               .replace('{EsA1 = }', 'EsA1 = ' + str(values['Task']['EsA1'])) \
               .replace('{EiA1 = }', 'EiA1 = ' + str(values['Task']['EiA1'])) \
               .replace('{EsA2 = }', 'EsA2 = ' + str(values['Task']['EsA2'])) \
               .replace('{EiA2 = }', 'EiA2 = ' + str(values['Task']['EiA2'])) \
               .replace('{EsA3 = }', 'EsA3 = ' + str(values['Task']['EsA3'])) \
               .replace('{EiA3 = }', 'EiA3 = ' + str(values['Task']['EiA3']))
    answer = { 'A4': values['Answer']['A4'], 'EsA4': values['Answer']['EsA4'], 'EiA4': values['Answer']['EiA4'] }
    return { text : dumps(answer) }

def __rk2_task3_prepare(text, values):
    text = text.replace('{TR2 = }', 'TR2 = ' + str(values['Task']['TR2'])) \
               .replace('{TR3 = }', 'TR3 = ' + str(values['Task']['TR3'])) \
               .replace('{TR4 = }', 'TR4 = ' + str(values['Task']['TR4']))
    answer = { 'TR1': values['Answer']['TR1'], 'TR1v': values['Answer']['TR1v'] }
    return { text : dumps(answer) }

#endregion

def load_tasks(filepath):
    try:
        with open(filepath, encoding='utf-8', mode='r') as fp:
            rk2_tasks = load(fp) 
        rk2_task1_text = rk2_tasks['Задание №1']
        rk2_task2_text = rk2_tasks['Задание №2']
        rk2_task3_text = rk2_tasks['Задание №3']
        rk2_task1_values = __rk2_task1_gen()
        rk2_task2_values = __rk2_task2_gen()
        rk2_task3_values = __rk2_task3_gen()
        result = {}
        rk2_task1 = __rk2_task1_prepare(rk2_task1_text, rk2_task1_values)
        result.update(rk2_task1)
        rk2_task2 = __rk2_task2_prepare(rk2_task2_text, rk2_task2_values)
        result.update(rk2_task2)
        rk2_task3 = __rk2_task3_prepare(rk2_task3_text, rk2_task3_values)
        result.update(rk2_task3)
        return result
    except Exception as error:
        return error