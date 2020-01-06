# By Kewth
'Kewth 喜欢的主题'
import os
import urllib.request
import colorama

def self_data(typ):
    if typ == 'init':
        self_data.score = 0
    elif typ == 'add':
        self_data.score += 100
    elif typ == 'get':
        return self_data.score

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

def lcs(str1, str2):
    'return the lenth of lcs of [str1] and [str2]'
    len1, len2 = len(str1), len(str2)
    if len1 == 0 or len2 == 0:
        return 0
    dpf = []
    for i in range(len1+1):
        lis = []
        for j in range(len2+1):
            lis.append(0)
        dpf.append(lis)
    for i in range(1, len1+1):
        for j in range(1, len2+1):
            if str1[i-1] == str2[j-1]:
                dpf[i][j] = dpf[i-1][j-1] + 1
            else:
                dpf[i][j] = max(dpf[i][j-1], dpf[i-1][j])
    return dpf[len1][len2]

def before_judge(problem):
    '''
    评测 [problem] 前
    若 [problem] 为空字符串则说明只有一题待评测
    '''
    print('先来条骚话')
    os.system('fortune > /tmp/say')
    os.system('lolcat /tmp/say')
    print()
    print('Judging {}'.format(problem))
    self_data('add')

def start():
    '所有评测开始前'
    self_data('init')

def end(score):
    '所有评测结束后，得分为 [score]'
    hitokoto = 'https://v1.hitokoto.cn?encode=text&charset=utf-8'
    print()
    print('再来条一言：')
    print(urllib.request.urlopen(hitokoto).readline().decode('utf-8'))
    print()
    print('哦差点忘了讲你得了 {} 分'.format(score))
    if score == 0:
        print('爆零了，菜鸡')
    elif score == self_data('get'):
        print('卧槽 AK 了 666')
    else:
        print('暴力都没拿满，NOI Day1 暴力 240 嘞！！')
