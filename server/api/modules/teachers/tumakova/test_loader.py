from random import gauss, randint, uniform, choice
from numpy import std, mean
from math import sqrt
from scipy import stats
from json import load, dumps

#region inner_gen_funcs
def __test_task1_gen():
  def __inner_gen__(mu, sigma, offset, n):
      x = [round(gauss(mu, sigma) + offset, 2) for i in range(n)]
      if n == 10:
        t = 2.26
      elif n == 12:
        t = 2.2
      else:
        t = 2.16
      s = std(x, ddof=1)  
      rand = t * (s / sqrt(n))
      sist = mean(x) - mu
      return {'Task': {'X': x, 'Xr': mu, 'n': n}, 'Answer': {'RandomError': rand, 'SistemError': sist}}
  return __inner_gen__(mu=randint(10, 100), sigma=uniform(0.1, 0.9), \
                       offset=uniform(0.1, 0.9), n=choice([10, 12, 14]))

def __test_task2_gen():
  def __inner_gen__(TD, Td, Sm):
    Tsn = sqrt(TD**2 + Td**2)
    z = (6*Sm) / Tsn
    F = stats.norm.cdf(z) - 0.5
    Ps = 0.5 + F
    Pn = 1 - Ps
    return {'Task':{'TD': TD, 'Td': Td, 'Sm': Sm}, 'Answer': {'Ps': Ps * 100, 'Pn': Pn * 100}}
  return __inner_gen__(TD=randint(20, 100), Td=randint(20, 100), Sm=randint(-20, 20))

def __test_task3_gen():
  def __inner_gen__(ES, EI, es, ei):
    TD = ES - EI
    Td = es - ei
    Tn = sqrt(TD**2 + Td**2)
    Nm = (es+ei)/2 - (ES+EI)/2
    Nmax = Nm + Tn / 2
    Nmin = Nm - Tn / 2
    return {'Task':{'ES': ES, 'EI': EI, 'es': es, 'ei': ei,}, \
            'Answer': {'Nmax': round(Nmax), 'Nmin': round(Nmin), 'Nm': round(Nm), 'Tn': round(Tn)}}
  ei = randint(0, 200)
  es = ei + randint(20, 100)
  ES = randint(-200, 0)
  EI = ES - randint(20, 100)
  return __inner_gen__(ES=ES, EI=EI, es=es, ei=ei)

def __test_task4_gen():
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

def __test_task5_gen():
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
    
def __test_task6_gen():
    def __inner_gen__(TR2, TR3, TR4):
        TR1 = TR2 + TR3 + TR4
        TR1v = round(sqrt(TR2**2 + TR3**2 + TR4**2))
        return {'Task': {'TR2': TR2, 'TR3': TR3, 'TR4': TR4}, \
                'Answer': {'TR1': TR1, 'TR1v': TR1v}}
    return __inner_gen__(TR2=randint(20, 100), TR3=randint(20, 100), TR4=randint(20, 100))
#endregion

#region inner_prepare_funcs
def __test_task1_prepare(text, values):
    text = text.replace('{X = []}', 'X = ' + str(values['Task']['X'])) \
               .replace('{Xr = }', 'Xr = ' + str(values['Task']['Xr'])) \
               .replace('{n = }', 'n = ' + str(values['Task']['n']))
    answer = { 'RE': round(values['Answer']['RandomError'], 2), \
               'SE': round(values['Answer']['SistemError'], 2) }
    return { text : dumps(answer) }
    
def __test_task2_prepare(text, values):
    text = text.replace('{TD = }', 'TD = ' + str(values['Task']['TD'])) \
               .replace('{Td = }', 'Td = ' + str(values['Task']['Td'])) \
               .replace('{Sm = }', 'Sm = ' + str(values['Task']['Sm']))
    answer = { 'Ps': round(values['Answer']['Ps']), \
               'Pn': round(values['Answer']['Pn']) }
    return { text : dumps(answer) }  

def __test_task3_prepare(text, values):
    text = text.replace('{ES = }', 'ES = ' + str(values['Task']['ES'])) \
               .replace('{EI = }', 'EI = ' + str(values['Task']['EI'])) \
               .replace('{es = }', 'es = ' + str(values['Task']['es'])) \
               .replace('{ei = }', 'ei = ' + str(values['Task']['ei']))
    answer = { 'Nmax': values['Answer']['Nmax'], 'Nmin': values['Answer']['Nmin'], \
               'Nm': values['Answer']['Nm'], 'Tn': values['Answer']['Tn'] }
    return { text : dumps(answer) }   
    
def __test_task4_prepare(text, values):
    text = text.replace('{D = }', 'D = ' + str(values['Task']['D'])) \
               .replace('{S = }', 'S = ' + str(values['Task']['S'])) \
               .replace('{EsD = }', 'EsD = ' + str(values['Task']['EsD'])) \
               .replace('{EiD = }', 'EiD = ' + str(values['Task']['EiD'])) \
               .replace('{EsS = }', 'EsS = ' + str(values['Task']['EsS'])) \
               .replace('{EiS = }', 'EiS = ' + str(values['Task']['EiS']))
    answer = { 'd': values['Answer']['d'], 'Esd': values['Answer']['Esd'], 'Eid': values['Answer']['Eid'] }
    return { text : dumps(answer) }
    
def __test_task5_prepare(text, values):
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

def __test_task6_prepare(text, values):
    text = text.replace('{TR2 = }', 'TR2 = ' + str(values['Task']['TR2'])) \
               .replace('{TR3 = }', 'TR3 = ' + str(values['Task']['TR3'])) \
               .replace('{TR4 = }', 'TR4 = ' + str(values['Task']['TR4']))
    answer = { 'TR1': values['Answer']['TR1'], 'TR1v': values['Answer']['TR1v'] }
    return { text : dumps(answer) }

#endregion

def load_tasks(filepath):
    try:
        with open(filepath, encoding='utf-8', mode='r') as fp:
            test_tasks = load(fp) 
        test_task1_text = test_tasks['Задание №1']
        test_task2_text = test_tasks['Задание №2']
        test_task3_text = test_tasks['Задание №3']
        test_task4_text = test_tasks['Задание №4']
        test_task5_text = test_tasks['Задание №5']
        test_task6_text = test_tasks['Задание №6']
        test_task1_values = __test_task1_gen()
        test_task2_values = __test_task2_gen()
        test_task3_values = __test_task3_gen()
        test_task4_values = __test_task4_gen()
        test_task5_values = __test_task5_gen()
        test_task6_values = __test_task6_gen()
        result = {}
        test_task1 = __test_task1_prepare(test_task1_text, test_task1_values)
        result.update(test_task1)
        test_task2 = __test_task2_prepare(test_task2_text, test_task2_values)
        result.update(test_task2)
        test_task3 = __test_task3_prepare(test_task3_text, test_task3_values)
        result.update(test_task3)
        test_task4 = __test_task4_prepare(test_task4_text, test_task4_values)
        result.update(test_task4)
        test_task5 = __test_task5_prepare(test_task5_text, test_task5_values)
        result.update(test_task5)
        test_task6 = __test_task6_prepare(test_task6_text, test_task6_values)
        result.update(test_task6)
        return result
    except Exception as error:
        return error

import asyncio
import concurrent.futures
from functools import partial

async def load_tasks_async(filepath):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
      result = await loop.run_in_executor(pool, partial(load_tasks, filepath))
      return result