from json import loads, dumps
import re
from api.modules.custom_exceptions import ContentError

class RK1_Checker():
    def __init__(self, correct_answer, answer):
        self.correct_answer = correct_answer
        self.answer = answer

    def __call__(self, index):
        try:
            correct_answer = loads(self.correct_answer)
            self.answer = self.answer.replace(',', '.').strip()
            spam = re.split('; |: |/ |;|:| |/|&', self.answer)
            if index == 1:
                if len(spam) != 2:
                    raise ContentError
                student_answer = { 'RE': float(spam[0]), 'SE': float(spam[1]) }
                RE_dif = (correct_answer['RE'] - student_answer['RE']) / correct_answer['RE']
                SE_dif = (correct_answer['SE'] - student_answer['SE']) / correct_answer['SE']
                if abs(RE_dif) <= 0.05 and abs(SE_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 2:
                if len(spam) != 1:
                    raise ContentError
                student_answer = { 'dF': float(spam[0]) }
                dF_dif = (correct_answer['dF'] - student_answer['dF']) / correct_answer['dF']
                if abs(dF_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
            elif index == 3:
                if len(spam) != 2:
                    raise ContentError
                if correct_answer['k1'] < correct_answer['k2']:
                    student_answer = { 'k1': float(spam[0]), 'k2': float(spam[1]) }
                elif correct_answer['k2'] < correct_answer['k1']:
                    student_answer = { 'k2': float(spam[0]), 'k1': float(spam[1]) }
                    student_answer = dict(sorted(student_answer.items(), key=lambda item: item[1]))
                else:
                    student_answer = { 'k1': float(spam[0]), 'k2': float(spam[1]) }
                k1_dif = (correct_answer['k1'] - student_answer['k1']) / correct_answer['k1']
                k2_dif = (correct_answer['k2'] - student_answer['k2']) / correct_answer['k2']
                if abs(k1_dif) <= 0.05 and abs(k2_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 4:
                if len(spam) != 2:
                    raise ContentError
                student_answer = { 'Ps': int(spam[0]), 'Pn': int(spam[1]) }
                Ps_dif = (correct_answer['Ps'] - student_answer['Ps']) / correct_answer['Ps']
                Pn_dif = (correct_answer['Pn'] - student_answer['Pn']) / correct_answer['Pn']
                if abs(Ps_dif) <= 0.05 and abs(Pn_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 5:
                if len(spam) != 1:
                    raise ContentError
                student_answer = { 'delta_instr': float(spam[0]) }
                delta_instr_dif = (correct_answer['delta_instr'] - student_answer['delta_instr']) / correct_answer['delta_instr']
                if abs(delta_instr_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
        except (ValueError, ContentError):
            return 0, self.answer

class RK2_Checker():
    def __init__(self, correct_answer, answer):
        self.correct_answer = correct_answer
        self.answer = answer

    def __call__(self, index):
        try:
            correct_answer = loads(self.correct_answer)
            self.answer = self.answer.replace(',', '.').strip()
            spam = re.split('/ |/|&', self.answer)
            if index == 1:
                if len(spam) < 1 and len(spam) > 2:
                    raise ContentError
                student_answer = { 'valid': spam[0].lower(), \
                                   'explanation': spam[1] if len(spam) == 2 else 'нет' }
                if student_answer['valid'] == correct_answer['valid']:
                    return 1, dumps(student_answer, ensure_ascii=False)
                else: 
                    return 0, dumps(student_answer, ensure_ascii=False)
            elif index == 2:
                if len(spam) < 3 and len(spam) > 4:
                    raise ContentError
                student_answer = { 'valid': [spam[0].lower(), spam[1].lower(), spam[2].lower()], \
                                   'explanation': spam[3] if len(spam) == 4 else 'нет' }
                score = 0
                for k in range(3):
                    if student_answer['valid'][k] == correct_answer['valid'][k]:
                        score += 1
                if score == 3:
                    return 1, dumps(student_answer, ensure_ascii=False)
                else:
                    return 0, dumps(student_answer, ensure_ascii=False)
            elif index == 3:
                if len(spam) < 1 and len(spam) > 2:
                    raise ContentError
                student_answer = { 'valid': spam[0].lower(), \
                                   'explanation': spam[1] if len(spam) == 2 else 'нет' }
                if student_answer['valid'] == correct_answer['valid']:
                    return 1, dumps(student_answer, ensure_ascii=False)
                else: 
                    return 0, dumps(student_answer, ensure_ascii=False) 
            elif index == 4:
                if len(spam) != 2:
                    raise ContentError
                student_answer = { 'Rkmin': float(spam[0]), 'Rkmax': float(spam[1]) }
                Rkmin_dif = (correct_answer['Rkmin'] - student_answer['Rkmin']) / correct_answer['Rkmin']
                Rkmax_dif = (correct_answer['Rkmax'] - student_answer['Rkmax']) / correct_answer['Rkmax']
                if abs(Rkmin_dif) <= 0.05 and abs(Rkmax_dif) <= 0.05:
                    return 2, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
        except (ValueError, ContentError):
            return 0, self.answer
    
class Test_Checker():
    def __init__(self, correct_answer, answer):
        self.correct_answer = correct_answer
        self.answer = answer

    def __call__(self, index):
        try:
            correct_answer = loads(self.correct_answer)
            self.answer = self.answer.replace(',', '.').strip()
            spam = re.split('; |: |/ |;|:| |/|&', self.answer)
            if index == 1:
                if len(spam) != 2:
                    raise ContentError
                student_answer = { 'RE': float(spam[0]), 'SE': float(spam[1]) }
                RE_dif = (correct_answer['RE'] - student_answer['RE']) / correct_answer['RE']
                SE_dif = (correct_answer['SE'] - student_answer['SE']) / correct_answer['SE']
                if abs(RE_dif) <= 0.05 and abs(SE_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 2:
                if len(spam) != 2:
                    raise ContentError
                student_answer = { 'Ps': int(spam[0]), 'Pn': int(spam[1]) }
                Ps_dif = (correct_answer['Ps'] - student_answer['Ps']) / correct_answer['Ps']
                Pn_dif = (correct_answer['Pn'] - student_answer['Pn']) / correct_answer['Pn']
                if abs(Ps_dif) <= 0.05 and abs(Pn_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 3:
                if len(spam) != 4:
                    raise ContentError
                student_answer = { 'Nmax': float(spam[0]), 'Nmin': float(spam[1]), \
                                   'Nm': float(spam[2]), 'Tn': float(spam[3]) }
                Nmax_dif = (correct_answer['Nmax'] - student_answer['Nmax']) / correct_answer['Nmax']
                Nmin_dif = (correct_answer['Nmin'] - student_answer['Nmin']) / correct_answer['Nmin']
                Nm_dif = (correct_answer['Nm'] - student_answer['Nm']) / correct_answer['Nm']
                Tn_dif = (correct_answer['Tn'] - student_answer['Tn']) / correct_answer['Tn']
                if abs(Nmax_dif) <= 0.05 and abs(Nmin_dif) <= 0.05 \
                   and abs(Nm_dif) <= 0.05 and abs(Tn_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
            if index == 4:
                if len(spam) != 3:
                    raise ContentError
                student_answer = { 'd': int(spam[0]), 'Esd': int(spam[1]), 'Eid': int(spam[2]) }
                if student_answer['d'] == correct_answer['d'] and \
                   student_answer['Esd'] == correct_answer['Esd'] and \
                   student_answer['Eid'] == correct_answer['Eid']:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 5:
                if len(spam) != 3:
                    raise ContentError
                student_answer = { 'A4': int(spam[0]), 'EsA4': int(spam[1]), 'EiA4': int(spam[2]) }
                if student_answer['A4'] == correct_answer['A4'] and \
                   student_answer['EsA4'] == correct_answer['EsA4'] and \
                   student_answer['EiA4'] == correct_answer['EiA4']:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
            elif index == 6:
                if len(spam) != 2:
                    raise ContentError
                student_answer = { 'TR1': int(spam[0]), 'TR1v': int(spam[1]) }
                if student_answer['TR1'] == correct_answer['TR1'] and \
                   student_answer['TR1v'] == correct_answer['TR1v']:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
        except (ValueError, ContentError):
            return 0, self.answer    