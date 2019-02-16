'打印测试点信息'

import colorama

def begin(id_x):
    '测 [id_x] 号测试点前'
    print('No.{:<4d} '.format(id_x), end='')

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
    print('{}{}Time Limit Error    {}'.format( \
            colorama.Back.WHITE, colorama.Fore.YELLOW, \
            colorama.Style.RESET_ALL), end=' ')

def test_ole():
    'OLE 信息'
    print('{}{}Output Limit Error  {} '.format( \
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
