from random import gauss, randint, uniform, choice
from collections import namedtuple
from numpy import mean, std
from json import load, dumps

#region inner_gen_funcs
def __rk2_task1_gen():
    def __inner_calculator__(d, P):
        H = 0.866025*P
        d2 = round(d - 2*(3/8)*H, 3)
        d1 = round(d - 2*(5/8)*H, 3)
        return d2, d1
    def __inner_gen__(thread_type, d, P, T, dr, d2r, d1r, fp, fa):
        valid = ''
        d2, d1 = __inner_calculator__(d, P)
        if thread_type == 'болт':
            dmax, dmin = d, d - T
            d2max, d2min = d2, d2 - T
            d1max = d1
            if dmin <= dr <= dmax and \
               d2r >= d2min and \
               d2r + fp + fa <= d2max and \
               d1r <= d1max:
               valid = 'годно'
            else:
               valid = 'брак'
        else:
            D, D2, D1 = d, d2, d1
            Dr, D2r, D1r = dr, d2r, d1r
            Dmin = D
            D2max, D2min = D2 + T, D2 
            D1max, D1min = D1 + T, D1
            if D1min <= D1r <= D1max and \
               D2r <= D2max and \
               D2r - fp - fa >= D2min and \
               Dr >= Dmin:
               valid = 'годно'
            else:
               valid = 'брак'
        return {'Task': {'type': thread_type, 'd': d, 'd2': d2, 'd1': d1, 'T': T, \
                'dr': dr, 'd2r': d2r, 'd1r': d1r, 'fp': fp, 'fa': fa}, \
                'Answer': {'valid': valid}
               }
    thread_type = choice(['гайка', 'болт'])
    d = randint(20, 60)
    P = randint(1,4)
    d2, d1 = __inner_calculator__(d, P)
    T = round(uniform(0.02, 0.1), 3)
    dr = round(d+uniform(-T/2, 0), 3) if thread_type == 'болт' else round(d+uniform(0, T/2), 3)
    d2r = round(d2+uniform(-T/2, 0), 3) if thread_type == 'болт' else round(d2+uniform(0, T/2), 3)
    d1r = round(d1+uniform(-T/2, 0), 3) if thread_type == 'болт' else round(d1+uniform(0, T/2), 3)
    return __inner_gen__(thread_type=thread_type, d=d, P=P, T=T, dr=dr, d2r=d2r, d1r=d1r, \
                         fp=round(uniform(0.005, 0.02), 3), fa=round(uniform(0.005, 0.02), 3))    

def __rk2_task2_gen():
    F = {'8': 80, '7': 70, '6': 60}
    f = {'8': 40, '7': 30, '6': 20}
    controlled_gear = namedtuple('gear', 'Fr fr')
    def __inner_gear_gen__():
        t = randint(6,8)
        p = randint(6,8)
        k = randint(6,8)
        jnmin = ['A','B','C','D','E','H']
        Tjn = ['a','b','c','d','e','h']
        if t == p and t == k:
            return str(t)+choice(jnmin)+choice(Tjn)
        else:
            return str(t)+"-"+str(p)+"-"+str(k)+choice(jnmin)+choice(Tjn)
    def __inner_gear_parse__(gear):
        if len(gear) > 3:
            t = gear[0]
            p = gear[2]
            k = gear[4]
            jnmin = gear[5]
            Tjn = gear[6]
        else:
            t = gear[0]
            p = t
            k = t
            jnmin = gear[1]
            Tjn = gear[2]
        return {'t': t, 'p': p, 'k': k, 'jnmin': jnmin, 'Tjn': Tjn}
    def __inner_task_gen__():
        gear = __inner_gear_gen__()
        gears = [controlled_gear(Fr=randint(55, 85), fr=randint(15, 45)) for i in range(3)]
        parsed_gear = __inner_gear_parse__(gear)
        check_lst = []                
        for g in gears:
            if g.Fr <= F[parsed_gear['t']] and g.fr <= f[parsed_gear['p']]:
                check_lst.append('годно')
            else:
                check_lst.append('брак')
        return {'Task': {'accuracy': gear, 'F': F, 'f': f, \
                         'gear1': (f'Fr={gears[0].Fr}', f'fr={gears[0].fr}'), \
                         'gear2': (f'Fr={gears[1].Fr}', f'fr={gears[1].fr}'), \
                         'gear3': (f'Fr={gears[2].Fr}', f'fr={gears[2].fr}')}, \
                         'Answer': {'valid': check_lst}
               }
    return __inner_task_gen__()
        
def __rk2_task3_gen():
    def __inner_gen__(mu, sigma, delta, T, n):
        valid = ''
        operand = choice(['+', '-'])
        if operand == '+':
            X = [round(gauss(mu, sigma) + delta, 3) for i in range(n)]
        if operand == '-':
            X = [round(gauss(mu, sigma) - delta, 3) for i in range(n)]
        P = choice([0.95, 0.99])
        if P == 0.95:
            k = 2
        else:
            k = 3
        Xmin = round(mu - T/2, 3)
        Xmax = round(mu + T/2, 3)
        Xqmin = round(mean(X) - k*std(X, ddof=1), 3)
        Xqmax = round(mean(X) + k*std(X, ddof=1), 3)
        if Xqmin >= Xmin and Xqmax <= Xmax:
            valid = 'годно'
        else:
            valid = 'брак'
        return {'Task': {'X': X, 'P': P, 'n': n, 'Xmin': Xmin, 'Xmax': Xmax}, \
                'Answer': {'valid': valid}
               }
    mu = randint(10,100)
    T = uniform(0.03,0.1)
    sigma = T/choice([4,5,6])
    delta = uniform(0.002,0.01)
    return __inner_gen__(mu=mu, sigma=sigma, delta=delta, T=T, n=randint(30,50))

def __rk2_task4_gen():
    def __inner_gen__(R, EsR, EiR):
        R1, R2, R3, Rs = R
        EsR1, EsR2, EsR3, EsRs = EsR
        EiR1, EiR2, EiR3, EiRs = EiR
        EmR1 = (EsR1+EiR1)/2
        EmR2 = (EsR2+EiR2)/2
        EmR3 = (EsR3+EiR3)/2
        EmRs = (EsRs+EiRs)/2
        TR1 = EsR1 - EiR1
        TR2 = EsR2 - EiR2
        TR3 = EsR3 - EiR3
        TRs = EsRs - EiRs
        R23 = R2*R3/(R2+R3)
        if (EmR2+EmR3) != 0:
            EmR23 = EmR2*EmR3/(EmR2+EmR3)
        else:
            EmR23 = 0
        TR23 = (R3/(R2+R3)-R2*R3/(R2+R3)**2)*TR2 + (R2/(R2+R3)-R2*R3/(R2+R3)**2)*TR3   
        Rk = Rs - (R1 + R23)
        Vk = TR1 + TR23 - TRs
        EmRk = EmRs-EmR1-EmR23
        EsRk = EmRk + Vk/2
        EiRk = EmRk - Vk/2
        Rkmin = Rk + EiRk
        Rkmax = Rk + EsRk
        return {'Task': {'R1': R[0], 'R2': R[1], 'R3': R[2], 'Rs': R[3], \
                         'EsR1': EsR[0], 'EsR2': EsR[1], 'EsR3': EsR[2], 'EsRs': EsR[3], \
                         'EiR1': EiR[0], 'EiR2': EiR[1], 'EiR3': EiR[2], 'EiRs': EiR[3]}, \
                'Answer': {'Rkmin': round(Rkmin, 1), 'Rkmax': round(Rkmax, 1)}
               }
    return __inner_gen__([randint(200,250), randint(200,250), randint(200,250), randint(400,500)], \
                         [round(uniform(1,2), 1), round(uniform(1,2), 1), \
                          round(uniform(1,2), 1), round(uniform(1,2), 1)], \
                         [round(uniform(-2,-1), 1), round(uniform(-2,-1), 1), \
                          round(uniform(-2,-1), 1), round(uniform(-2,-1), 1)])
#endregion

#region inner_prepare_funcs
def __rk2_task1_prepare(text, values):
    text = text.replace('{d(D) = }', 'd(D) = ' + str(values['Task']['d'])) \
               .replace('{d2(D2) = }', 'd2(D2) = ' + str(values['Task']['d2'])) \
               .replace('{d1(D1) = }', 'd1(D1) = ' + str(values['Task']['d1'])) \
               .replace('{T = }', 'T = ' + str(values['Task']['T'])) \
               .replace('{ }', str(values['Task']['type'])) \
               .replace('{dr(Dr) = }', 'dr(Dr) = ' + str(values['Task']['dr'])) \
               .replace('{d2r(D2r) = }', 'd2r(D2r) = ' + str(values['Task']['d2r'])) \
               .replace('{d1r(D1r) = }', 'd1r(D1r) = ' + str(values['Task']['d1r'])) \
               .replace('{fp = }', 'fp = ' + str(values['Task']['fp'])) \
               .replace('{fa = }', 'fa = ' + str(values['Task']['fa']))   
    answer = { 'valid': values['Answer']['valid'] }
    return { text : dumps(answer, ensure_ascii=False) }
    
def __rk2_task2_prepare(text, values):
    text = text.replace('{ }', str(values['Task']['accuracy'])) \
               .replace('{F = }', 'F = ' + str(values['Task']['F'])) \
               .replace('{f = }', 'f = ' + str(values['Task']['f'])) \
               .replace('{Колесо 1 = }', 'Колесо 1 = ' + str(values['Task']['gear1'])) \
               .replace('{Колесо 2 = }', 'Колесо 2 = ' + str(values['Task']['gear2'])) \
               .replace('{Колесо 3 = }', 'Колесо 3 = ' + str(values['Task']['gear3'])) 
    answer = { 'valid': values['Answer']['valid'] }
    return { text : dumps(answer, ensure_ascii=False) }

def __rk2_task3_prepare(text, values):
    text = text.replace('{n = }', 'n = ' + str(values['Task']['n'])) \
               .replace('{X = []}', 'X = ' + str(values['Task']['X'])) \
               .replace('{[]}', '[' + str(values['Task']['Xmin']) + '; ' + str(values['Task']['Xmax']) + ']') \
               .replace('{P = }', 'P = ' + str(values['Task']['P']))
    answer = { 'valid': values['Answer']['valid'] }
    return { text : dumps(answer, ensure_ascii=False) }

def __rk2_task4_prepare(text, values):
    text = text.replace('{R1 = }', 'R1 = ' + str(values['Task']['R1'])) \
               .replace('{EsR1 = }', 'EsR1 = ' + str(values['Task']['EsR1'])) \
               .replace('{EiR1 = }', 'EiR1 = ' + str(values['Task']['EiR1'])) \
               .replace('{R2 = }', 'R2 = ' + str(values['Task']['R2'])) \
               .replace('{EsR2 = }', 'EsR2 = ' + str(values['Task']['EsR2'])) \
               .replace('{EiR2 = }', 'EiR2 = ' + str(values['Task']['EiR2'])) \
               .replace('{R3 = }', 'R3 = ' + str(values['Task']['R3'])) \
               .replace('{EsR3 = }', 'EsR3 = ' + str(values['Task']['EsR3'])) \
               .replace('{EiR3 = }', 'EiR3 = ' + str(values['Task']['EiR3'])) \
               .replace('{Rsum = }', 'Rsum = ' + str(values['Task']['Rs'])) \
               .replace('{EsRsum = }', 'EsRsum = ' + str(values['Task']['EsRs'])) \
               .replace('{EiRsum = }', 'EiRsum = ' + str(values['Task']['EiRs']))  
    answer = { 'Rkmin': values['Answer']['Rkmin'], 'Rkmax': values['Answer']['Rkmax'] }
    return { text : dumps(answer) }
#endregion

def load_tasks(filepath):
    try:
        with open(filepath, encoding='utf-8', mode='r') as fp:
            rk2_tasks = load(fp) 
        rk2_task1_text = rk2_tasks['Задание №1']
        rk2_task2_text = rk2_tasks['Задание №2']
        rk2_task3_text = rk2_tasks['Задание №3']
        rk2_task4_text = rk2_tasks['Задание №4']
        rk2_task1_values = __rk2_task1_gen()
        rk2_task2_values = __rk2_task2_gen()
        rk2_task3_values = __rk2_task3_gen()
        rk2_task4_values = __rk2_task4_gen()
        result = {}
        rk2_task1 = __rk2_task1_prepare(rk2_task1_text, rk2_task1_values)
        result.update(rk2_task1)
        rk2_task2 = __rk2_task2_prepare(rk2_task2_text, rk2_task2_values)
        result.update(rk2_task2)
        rk2_task3 = __rk2_task3_prepare(rk2_task3_text, rk2_task3_values)
        result.update(rk2_task3)
        rk2_task4 = __rk2_task4_prepare(rk2_task4_text, rk2_task4_values)
        result.update(rk2_task4)
        return result
    except Exception as error:
        return error