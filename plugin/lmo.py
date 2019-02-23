# By ld_liaomo
'lmo 喜欢的输出方式，可以双手玩五阶魔方倒走钢丝倒背民法。'

import colorama
import random
import urllib.request

def begin(id_x):
    '测 [id_x] 号测试点前'
    print('#{} '.format(id_x), end='')

def end_case(typ):
    '测完一个测试点后，该测试点状态为 [typ]'
    print()

def runtime(use):
    '运行时间 [use] ms'
    print(' time:{}'.format(use), end='')

def exitstatus(ret):
    'RE 返回 [ret]'
    # 因为 ntest 太萎了，所以这个返回值要右移 8 位。
    print(' statu:{}'.format(ret >> 8), end='')

def test_ac():
    'AC 信息'
    print('{}{}✔{}'.format(colorama.Style.BRIGHT, colorama.Fore.GREEN, \
    	    colorama.Style.RESET_ALL), end=' ')

def test_wa():
    'WA 信息'
    print('{}{}✘{}'.format(colorama.Style.BRIGHT, colorama.Fore.RED, \
    	    colorama.Style.RESET_ALL), end=' ')

def test_re():
    'RE 信息'
    print('{}{}♡{}'.format(colorama.Style.BRIGHT, \
		    colorama.Fore.MAGENTA, colorama.Style.RESET_ALL), end=' ')

def test_tle():
    'TLE 信息'
    print('{}{}♨{}'.format(colorama.Style.BRIGHT, \
		    colorama.Fore.CYAN, colorama.Style.RESET_ALL), end=' ')

def test_ole():
    'OLE 信息'
    print('☠', end=' ')

def test_uke():
    'UKE 信息'
    print('它 UKE 了，快点去嘲讽万大师。')

def test_pa():
    'PA 信息'
    print('{}{}Partially Accept    {}'.format( \
    	    colorama.Back.WHITE, colorama.Fore.GREEN, \
    	    colorama.Style.RESET_ALL), end=' ')

def before_judge(problem):
    '''
    评测 [problem] 前
    若 [problem] 为空字符串则说明只有一题待评测
    '''
    print('正在评测{}'.format(problem))

def start():
    '所有评测开始前'
    print('我要妹子。　　——鲁迅')
    #pass

def end(score):
    '所有评测结束后，得分为 [score]'
    if random.randint(1, 6) >= 6:
        hitokoto = 'https://v1.hitokoto.cn?encode=text&charset=utf-8'
        print('这是六分之一的概率一言~')
        print(urllib.request.urlopen(hitokoto).readline().decode('utf-8'))
    print('score: {}'.format(score))
