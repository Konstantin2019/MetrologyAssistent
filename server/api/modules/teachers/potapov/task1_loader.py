from random import gauss, randint, uniform, choice
from numpy import std, mean
from math import sqrt
from scipy import stats
from json import load, dumps

#region inner_gen_funcs
def __rk1_task1_gen():
  def __inner_gen__(mu, sigma, offset, n):
      x = [round(gauss(mu, sigma) + offset, 2) for i in range(n)]
      P = choice([0.95, 0.99])
      if P == 0.95:
        k = 2
      else:
        k = 3
      s = std(x, ddof=1)  
      rand = k * (s / sqrt(n))
      sist = mean(x) - mu
      return {'Task': {'X': x, 'Xr': mu, 'P': P}, 'Answer': {'RandomError': rand, 'SistemError': sist}}
  return __inner_gen__(mu=randint(10, 100), sigma=uniform(0.1, 0.9), offset=uniform(0.1, 0.9), n=10)

def __rk1_task2_gen():
  def __inner_gen__(params1, params2, params3):
    flag = [True, False]
    rand = "Случайная" if choice(flag) is True else "Систематическая"
    a,b,c,d = params1
    x,y,z = params2
    da, db, dc, dd = params3
    F = f'a^{x:.2f}+b^{y:.2f}+c^{z:.2f}+d'
    dF_da = x*pow(a, x-1)
    dF_db = y*pow(b, y-1)
    dF_dc = z*pow(c, z-1)
    dF_dd = 1
    if rand is False:
      dF = dF_da * da + dF_db * db + dF_dc * dc + dF_dd * dd
    else:
      dF = sqrt((dF_da * da)**2 + (dF_db * db)**2 + (dF_dc * dc)**2 + (dF_dd * dd)**2)
    return {'Task':{'Function': F, 'Random error': rand, 'abcd': (a, b, c, d), \
            'xyz':(round(x, 2), round(y, 2), round(z, 2)), \
            'da_db_dc_dd': (round(da, 2), round(db, 2), round(dc, 2), round(dd, 2)) }, \
            'Answer': {'dF': dF}}
  p1 = (randint(1,20), randint(1,20), randint(1,20), randint(1,20))
  p2 = (uniform(0,4), uniform(0,4), uniform(0,4))
  p3 = (uniform(0,0.1), uniform(0,0.1), uniform(0,0.1), uniform(0,0.1))
  return __inner_gen__(params1=p1, params2=p2, params3=p3)

def __rk1_task3_gen():
  def __inner_gen__(L1, L2, T1, T2):
    i1 = 0.45*pow(L1,(1/3)) + 0.001*L1
    i2 = 0.45*pow(L2,(1/3)) + 0.001*L2
    k1 = T1 / i1
    k2 = T2 / i2
    return {'Task': {'L1': L1, 'L2': L2, 'T1': T1, 'T2': T2}, 'Answer': {'k1': k1, 'k2': k2}}
  return __inner_gen__(L1=randint(10, 500), L2=randint(10, 500), T1=randint(20, 300), T2=randint(20, 300))

def __rk1_task4_gen():
  def __inner_gen__(TD, Td, Sm):
    Tsn = sqrt(TD**2 + Td**2)
    z = (6*Sm) / Tsn
    F = stats.norm.cdf(z) - 0.5
    Ps = 0.5 + F
    Pn = 1 - Ps
    return {'Task':{'TD': TD, 'Td': Td, 'Sm': Sm}, 'Answer': {'Ps': Ps * 100, 'Pn': Pn * 100}}
  return __inner_gen__(TD=randint(20, 100), Td=randint(20, 100), Sm=randint(-20, 20))

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
               .replace('{P = }', 'P = ' + str(values['Task']['P']))
    answer = { 'RE': round(values['Answer']['RandomError'], 2), \
               'SE': round(values['Answer']['SistemError'], 2) }
    return { text : dumps(answer) }
    
def __rk1_task2_prepare(text, values):
    text = text.replace('{F = a^x + b^y + c^z + d}', 'F = ' + str(values['Task']['Function'])) \
               .replace('{a,b,c,d = }', 'a,b,c,d = ' + str(values['Task']['abcd'])) \
               .replace('{x,y,z = }', 'x,y,z = ' + str(values['Task']['xyz'])) \
               .replace('{da,db,dc,dd = }', 'da,db,dc,dd = ' + str(values['Task']['da_db_dc_dd'])) \
               .replace('{Тип погрешностей : }', 'Тип погрешностей : ' + str(values['Task']['Random error']))    
    answer = { 'dF': round(values['Answer']['dF'], 2) }
    return { text : dumps(answer) }      

def __rk1_task3_prepare(text, values):
    text = text.replace('{L1 = }', 'L1 = ' + str(values['Task']['L1'])) \
               .replace('{L2 = }', 'L2 = ' + str(values['Task']['L2'])) \
               .replace('{T1 = }', 'T1 = ' + str(values['Task']['T1'])) \
               .replace('{T2 = }', 'T2 = ' + str(values['Task']['T2']))
    answer = { 'k1': round(values['Answer']['k1'], 2), \
               'k2': round(values['Answer']['k2'], 2) }
    return { text : dumps(answer) }

def __rk1_task4_prepare(text, values):
    text = text.replace('{TD = }', 'TD = ' + str(values['Task']['TD'])) \
               .replace('{Td = }', 'Td = ' + str(values['Task']['Td'])) \
               .replace('{Sm = }', 'Sm = ' + str(values['Task']['Sm']))
    answer = { 'Ps': round(values['Answer']['Ps']), \
               'Pn': round(values['Answer']['Pn']) }
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