from random import gauss, randint, uniform, choice
from numpy import std, mean
from math import sqrt
from json import load, dumps

#region inner_gen_funcs
def __rk1_task1_gen():
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

def __rk1_task2_gen():
  def __inner_gen__(ES, EI, es, ei):
    Smax = ES - ei
    Smin = EI - es
    Sm = (Smax + Smin) / 2
    Ts = Smax - Smin
    return {'Task':{'ES': ES, 'EI': EI, 'es': es, 'ei': ei,}, \
            'Answer': {'Smax': Smax, 'Smin': Smin, 'Sm': round(Sm), 'Ts': Ts}}
  EI = randint(0, 200)
  ES = EI + randint(20, 100)
  es = randint(-200, 0)
  ei = es - randint(20, 100)
  return __inner_gen__(ES=ES, EI=EI, es=es, ei=ei)

def __rk1_task3_gen():
  def __inner_gen__(L1, L2, T1, T2):
    i1 = 0.45*pow(L1,(1/3)) + 0.001*L1
    i2 = 0.45*pow(L2,(1/3)) + 0.001*L2
    k1 = T1 / i1
    k2 = T2 / i2
    return {'Task': {'L1': L1, 'L2': L2, 'T1': T1, 'T2': T2}, 'Answer': {'k1': k1, 'k2': k2}}
  return __inner_gen__(L1=randint(10, 500), L2=randint(10, 500), T1=randint(20, 300), T2=randint(20, 300))

def __rk1_task4_gen():
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

def __rk1_task5_gen():
    def __inner_gen__(T, Ametr, delta_met, delta_sub):
      delta = Ametr*T
      delta_instr = delta - (delta_met * delta) / 100 - (delta_sub * delta) / 100
      return {'Task': {'T': T, 'Ametr': Ametr, 'delta_met': delta_met, 'delta_sub': delta_sub}, \
              'Answer': {'delta_instr': delta_instr}}
    return __inner_gen__(T=randint(20, 100), Ametr=choice([0.2, 0.25, 0.3, 0.35]), \
                         delta_met=randint(5, 40), delta_sub=randint(1, 10))
#endregion

#region inner_prepare_funcs
def __rk1_task1_prepare(text, values):
    text = text.replace('{X = []}', 'X = ' + str(values['Task']['X'])) \
               .replace('{Xr = }', 'Xr = ' + str(values['Task']['Xr'])) \
               .replace('{n = }', 'n = ' + str(values['Task']['n']))
    answer = { 'RE': round(values['Answer']['RandomError'], 2), \
               'SE': round(values['Answer']['SistemError'], 2) }
    return { text : dumps(answer) }
    
def __rk1_task2_prepare(text, values):
    text = text.replace('{ES = }', 'ES = ' + str(values['Task']['ES'])) \
               .replace('{EI = }', 'EI = ' + str(values['Task']['EI'])) \
               .replace('{es = }', 'es = ' + str(values['Task']['es'])) \
               .replace('{ei = }', 'ei = ' + str(values['Task']['ei']))
    answer = { 'Smax': values['Answer']['Smax'], 'Smin': values['Answer']['Smin'], \
               'Sm': values['Answer']['Sm'], 'Ts': values['Answer']['Ts'] }
    return { text : dumps(answer) }      

def __rk1_task3_prepare(text, values):
    text = text.replace('{L1 = }', 'L1 = ' + str(values['Task']['L1'])) \
               .replace('{L2 = }', 'L2 = ' + str(values['Task']['L2'])) \
               .replace('{T1 = }', 'T1 = ' + str(values['Task']['T1'])) \
               .replace('{T2 = }', 'T2 = ' + str(values['Task']['T2']))
    answer = { 'k1': round(values['Answer']['k1'], 1), \
               'k2': round(values['Answer']['k2'], 1) }
    return { text : dumps(answer) }

def __rk1_task4_prepare(text, values):
    text = text.replace('{ES = }', 'ES = ' + str(values['Task']['ES'])) \
               .replace('{EI = }', 'EI = ' + str(values['Task']['EI'])) \
               .replace('{es = }', 'es = ' + str(values['Task']['es'])) \
               .replace('{ei = }', 'ei = ' + str(values['Task']['ei']))
    answer = { 'Nmax': values['Answer']['Nmax'], 'Nmin': values['Answer']['Nmin'], \
               'Nm': values['Answer']['Nm'], 'Tn': values['Answer']['Tn'] }
    return { text : dumps(answer) }   

def __rk1_task5_prepare(text, values):
    text = text.replace('{T = }', 'T = ' + str(values['Task']['T'])) \
               .replace('{Ametr = }', 'Ametr = ' + str(values['Task']['Ametr'])) \
               .replace('{delta_met = }', 'delta_met = ' + str(values['Task']['delta_met'])) \
               .replace('{delta_sub = }', 'delta_sub = ' + str(values['Task']['delta_sub']))
    answer = { 'delta_instr': round(values['Answer']['delta_instr'], 1) }
    return { text : dumps(answer) }
#endregion

def load_tasks(filepath):
    try:
        with open(filepath, encoding='utf-8', mode='r') as fp:
            rk1_tasks = load(fp) 
        rk1_task1_text = rk1_tasks['Задание №1']
        rk1_task2_text = rk1_tasks['Задание №2']
        rk1_task3_text = rk1_tasks['Задание №3']
        rk1_task4_text = rk1_tasks['Задание №4']
        rk1_task5_text = rk1_tasks['Задание №5']
        rk1_task1_values = __rk1_task1_gen()
        rk1_task2_values = __rk1_task2_gen()
        rk1_task3_values = __rk1_task3_gen()
        rk1_task4_values = __rk1_task4_gen()
        rk1_task5_values = __rk1_task5_gen()
        result = {}
        rk1_task1 = __rk1_task1_prepare(rk1_task1_text, rk1_task1_values)
        result.update(rk1_task1)
        rk1_task2 = __rk1_task2_prepare(rk1_task2_text, rk1_task2_values)
        result.update(rk1_task2)
        rk1_task3 = __rk1_task3_prepare(rk1_task3_text, rk1_task3_values)
        result.update(rk1_task3)
        rk1_task4 = __rk1_task4_prepare(rk1_task4_text, rk1_task4_values)
        result.update(rk1_task4)
        rk1_task5 = __rk1_task5_prepare(rk1_task5_text, rk1_task5_values)
        result.update(rk1_task5)
        return result
    except Exception as error:
        return error