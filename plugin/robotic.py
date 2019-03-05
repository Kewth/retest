# By ld_liaomo
'使 retest 的输出适于其他程序处理。'

import colorama

def begin(id_x):
    '测 [id_x] 号测试点前'
    print('no={:<4d} '.format(id_x), end='')

def end_case(typ):
    '测完一个测试点后，该测试点状态为 [typ]'
    print()

def runtime(use):
    '运行时间 [use] ms'
    print(' time={}'.format(use), end='')

def exitstatus(ret):
    'RE 返回 [ret]'
    print(' exit={}'.format(ret), end='')

def test_ac():
    'AC 信息'
    print(' AC', end='')

def test_wa():
    'WA 信息'
    print(' WA', end='')

def test_re():
    'RE 信息'
    print(' RE', end='')

def test_tle():
    'TLE 信息'
    print(' TLE', end='')

def test_mle():
    'MLE 信息'
    print(' MLE', end='')

def test_ole():
    'OLE 信息'
    print(' OLE', end='')

def test_uke():
    'UKE 信息'
    print(' UKE', end='')
def test_pa():
    'PA 信息'
    print(' PA', end='')

def before_judge(problem):
    '''
    评测 [problem] 前
    若 [problem] 为空字符串则说明只有一题待评测
    '''
    # print('Judging {}'.format(problem))

def start():
    '所有评测开始前'
    print('START')

def end(score):
    '所有评测结束后，得分为 [score]'
    print('score={}'.format(score))
    print('END')
