'''
打印测试点信息
默认使用
有所有接口，可作为参考
'''

import colorama

def begin(id_x):
    '测 [id_x] 号测试点前'
    print('No.{:<4d} '.format(id_x), end='')

def end_case(typ):
    '测完一个测试点后，该测试点状态为 [typ]'
    print()

def runtime(use):
    '运行时间 [use] ms'
    print('RunTime:', use, 'ms', end='')

def exitstatus(ret):
    'RE 返回 [ret]'
    print('Exit status:', ret, end='')

def test_ac():
    'AC 信息'
    print('{}{}Accept              {}'.format( \
            colorama.Back.BLACK, colorama.Fore.GREEN, \
            colorama.Style.RESET_ALL), end=' ')

def test_wa():
    'WA 信息'
    print('{}{}Wrong Answer        {}'.format( \
            colorama.Back.BLACK, colorama.Fore.RED, \
            colorama.Style.RESET_ALL), end=' ')

def test_re():
    'RE 信息'
    print('{}{}Runtime Error       {}'.format( \
            colorama.Back.BLACK, colorama.Fore.MAGENTA, \
            colorama.Style.RESET_ALL), end=' ')

def test_tle():
    'TLE 信息'
    print('{}{}Time Limit Exceeded    {}'.format( \
            colorama.Back.WHITE, colorama.Fore.YELLOW, \
            colorama.Style.RESET_ALL), end=' ')

def test_mle():
    'MLE 信息'
    print('{}{}Memory Limit Exceeded  {}'.format( \
            colorama.Back.WHITE, colorama.Fore.MAGENTA, \
            colorama.Style.RESET_ALL), end=' ')

def test_ole():
    'OLE 信息'
    print('{}{}Output Limit Exceeded  {} '.format( \
            colorama.Back.WHITE, colorama.Fore.RED, \
            colorama.Style.RESET_ALL), end=' ')

def test_uke():
    'UKE 信息'
    print('{}{}Unknown Error       {} '.format( \
            colorama.Back.WHITE, colorama.Fore.BLACK, \
            colorama.Style.RESET_ALL), end=' ')

def test_pa():
    'PA 信息'
    print('{}{}Partially Accept    {}'.format( \
            colorama.Back.WHITE, colorama.Fore.GREEN, \
            colorama.Style.RESET_ALL), end=' ')
    # 如果希望输出分数，读取 sp.get 即可
    print('score:{} '.format(int(open('sp.get', 'r').readline().replace('\n', ''))),\
            end='')

def before_judge(problem):
    '''
    评测 [problem] 前
    若 [problem] 为空字符串则说明只有一题待评测
    '''
    print('Judging {}'.format(problem))

def start():
    '所有评测开始前'
    pass

def end(score):
    '所有评测结束后，得分为 [score]'
    print('score: {}'.format(score))
    print('\n\nSee more message in retest_dir\n\n')
    print('Made by Kewth', '(c)')
    print('Thanks', 'for', 'using', 'retest')
