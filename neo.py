#!/usr/bin/python3
'新的 retest'

import sys
import os
import shutil
import argparse
import yaml
import colorama

PATH = './retest_dir'
TIMEOUT = os.system('timeout 0.1 sleep 1')

def read_data(data):
    '''
    在工作目录创建输入输出文件（源于 [data] ）
    返回所有数据文件的名字
    '''
    files = os.listdir(data)
    num = 0
    res = [None]
    for i in files:
        if i.rfind('.in') + 3 == len(i):
            name = i[:-3]
            outname = ''
            if name + '.out' in files:
                outname = '.out'
            elif name + '.ans' in files:
                outname = '.ans'
            if outname == '':
                continue
            num += 1
            up_path = '.'
            for j in range(PATH.count('/')):
                up_path += '/..'
            os.system('ln -s {}/{}/{}{} {}/{}.in'.format( \
                    up_path, data, name, '.in', PATH, num))
            os.system('ln -s {}/{}/{}{} {}/{}.ans'.format( \
                    up_path, data, name, outname, PATH, num))
            res.append(name)
    return res

def error_exit(info):
    '打印错误信息并退出'
    print(colorama.Fore.RED, info, \
            colorama.Fore.RESET, file=sys.stderr)
    shutil.rmtree('retest_dir')
    sys.exit(1)

def warning(info):
    '打印警告信息'
    print(colorama.Fore.YELLOW, 'Warning: ' + info, \
            colorama.Fore.RESET, file=sys.stderr)

def get_config():
    '''
    获取配置信息
    返回一个字典
    '''
    home_dir = os.path.expandvars('$HOME') + '/.config/retest/'
    config_file = open(home_dir + 'retest.yaml', 'r')
    res = yaml.load(config_file)
    try:
        config_file = open('retest.yaml', 'r')
    except FileNotFoundError:
        error_exit('No retest.yaml was found, input ntest -h to get help')
    current_dict = yaml.load(config_file)
    for key in current_dict:
        # 用全局配置更新局部配置
        res[key] = current_dict[key]
    return res

def print_info(typ, i):
    '打印 [i] 号测试点信息（类型为 [typ]）'
    print('No.{:<4d} '.format(i), end='')
    if typ == 'AC':
        print(colorama.Back.GREEN, colorama.Fore.WHITE, \
                'Accept            ', colorama.Style.RESET_ALL)
    elif typ == 'WA':
        print(colorama.Back.RED, colorama.Fore.WHITE, \
                'Wrong Answer      ', colorama.Style.RESET_ALL)
    elif typ == 'RE':
        print(colorama.Back.MAGENTA, colorama.Fore.WHITE, \
                'Runtime Error     ', colorama.Style.RESET_ALL)
    elif typ == 'TLE':
        print(colorama.Back.WHITE, colorama.Fore.YELLOW, \
                'Time Limit Error  ', colorama.Style.RESET_ALL)
    elif typ == 'OLE':
        print(colorama.Back.WHITE, colorama.Fore.RED, \
                'Output Limit Error', colorama.Style.RESET_ALL)
    elif typ == 'UKE':
        print(colorama.Back.BLACK, colorama.Fore.RED, \
                'Unknown Error     ', colorama.Style.RESET_ALL)
    elif typ == 'PA':
        print(colorama.Back.GREEN, colorama.Fore.RED, \
                'Partially Accept  ', colorama.Style.RESET_ALL)

def compile_cpp(name, exe, compiler):
    '用 [compiler] 编译程序 [name] 到工作目录的 [exe]'
    res = os.system('{} {} -o {}/{}'.format(compiler, name, PATH, exe))
    if res != 0:
        error_exit('Compile Error')

def make_dir():
    '强行创建工作基目录'
    if os.path.exists('retest_dir'):
        warning('The directory {} has exist'.format('retest_dir'))
        shutil.rmtree('retest_dir')
    os.makedirs('retest_dir')

def init_args():
    '初始化参数'
    parser = argparse.ArgumentParser(description='''
A retest command which is like lemon but run in terminal.
And this is the upgraded version of retest
''')
    parser.add_argument('-l', '--learn', action='store_true', \
            help='learn how to use ntest')
    return parser.parse_args()

def learn(): # {{{
    '--learn 的信息'
    print('''
How to write retest.yaml?
    The file retest.yaml is used by ntest to judge.
    You can get a full example on ~/.config/retest/example.yaml .

    source: (required)
        The source code you want to judge.

    data: (required)
        The directory where include all data files.

    time:
        The time limit of each judgement.
        Its unit is millisecond.
        It's set to 1000 by default.

    difftime:
        The time limit of checking answer.
        Its unit is millisecond.
        It's set to 1000 by default.

    input:
        The file where exe get input.

    output:
        The file where exe get output.

    If you want to judge more problems, you can set 'Tn' sub configura
  tion.
        For example:
            time: 1000
            T1:
                source: a.cpp
                data: data/A
            T2:
                source: b.cpp
                data: data/B
        It will judge 2 problems in one time.

Some usefull arguments:
    You can rough understanding by using 'ntest -h' or 'ntest --help'.

    --learn, -l:
        Print this message to learn how to use ntest.
        To display this better, you can use 'less' command:
            ntest -l | less
    ''')
# }}}

def check_config(config):
    '检查配置字典 [config] 的合法性'
    if not config.get('source'):
        error_exit('No source was read')
    if not config.get('data'):
        error_exit('No data was read')
    if not config.get('time'):
        config['time'] = 1000
    if not config.get('difftime'):
        config['difftime'] = 1000
    # if not config.get('mode'):
    #     config['mode'] = 'tradition'
    # 在工作目录制造用于评分的 spj
    if not config.get('spj'):
        os.system('cp ~/.config/retest/spj {}/spj'.format(PATH))
    elif len(config['spj']) > 4 and config['spj'][-4:] == '.cpp':
        compile_cpp(config['spj'], 'spj', 'g++')
    elif len(config['spj']) > 2 and config['spj'][-2:] == '.c':
        compile_cpp(config['spj'], 'spj', 'gcc')
    else:
        os.system('cp {} {}/spj'.format(config['spj'], PATH))
    # 在工作目录制造用于运行的 exe
    if len(config['source']) > 4 and config['source'][-4:] == '.cpp':
        compile_cpp(config['source'], 'exe', 'g++')
    elif len(config['source']) > 2 and config['source'][-2:] == '.c':
        compile_cpp(config['source'], 'exe', 'gcc')
    else:
        os.system('cp {} {}/exe'.format(config['source'], PATH))

def check_ans_spj(config, i, score):
    '''
    在工作目录用 spj 进行测试（测试点编号为 [i] ）
    以 [config] 为配置
    返回得分
    '''
    spres = os.system( \
            'timeout {2} ./spj \
            {0}.in {0}.out {0}.ans {1} sp.get sp.log'.format( \
            i, score, config['difftime']))
    # 评分过程超时
    if spres == TIMEOUT:
        print_info('OLE', i)
        print('Output too long', file=open('res{}'.format(i), 'a'))
    # 评分过程错误
    elif spres != 0:
        print_info('UKE', i)
    get = float(open('sp.get', 'r').readline()[:-1])
    # 正确
    if get == score:
        print_info('AC', i)
        print('Accept', file=open('res{}'.format(i), 'w'))
    # 错误
    elif get == 0:
        print_info('WA', i)
    # 部分正确
    else:
        print_info('PA', i)
    print('\nMessage from spj:', file=open('res{}'.format(i), 'a'))
    os.system('cat sp.log >> res{}'.format(i))
    return get

def judge(config):
    '''
    评测一道题目，以 [config] 为配置
    返回该题目的分数
    '''
    check_config(config)
    files = read_data(config['data'])
    num = len(files)
    res = 0
    os.chdir(PATH)
    for i in range(1, num):
        # 评测单个测试点
        if config.get('input'):
            os.system('ln -sf {}.in {}'.format( \
                    i, config['input']))
        if config.get('output'):
            os.system('ln -sf {}.out {}'.format( \
                    i, config['output']))
        runres = os.system( \
                'timeout {0} ./exe < {1}.in > {1}.out'.format( \
                config['time'] / 1000, i))
        # 程序超时（没有输出）
        if runres == TIMEOUT:
            print_info('TLE', i)
            continue
        # 程序运行时错误（没有输出）
        elif runres != 0:
            print_info('RE', i)
            print('exe return {}'.format(runres))
            continue
        res += check_ans_spj(config, i, 100 / (num - 1))
    for i in range(PATH.count('/')):
        os.chdir('..')
    return int(res)

def main():
    '主函数'
    args = init_args()
    if args.learn:
        learn()
    config = get_config()
    now = 0
    while config.get('T{}'.format(now + 1)):
        now += 1
    make_dir()
    if now != 0:
        # 有多个程序待评测
        score = 0
        for i in range(1, now + 1):
            problem = 'T{}'.format(i)
            global PATH
            PATH = './retest_dir/' + problem
            print('Judging {}'.format(problem))
            os.makedirs('retest_dir/' + problem)
            sub_config = config[problem]
            for key in config:
                # 用全局配置更新局部配置
                if not sub_config.get(key):
                    sub_config[key] = config[key]
            score += judge(sub_config)
    else:
        print('Judging')
        score = judge(config)
    print('score: {}'.format(score))
    return 0

RES = main()
print('\n\nSee more message in retest_dir\n\n')
print('Made by Kewth', '(c)')
print('Press', 'Ctrl-c', 'to', 'forcefully', 'exit')
print('Thanks', 'for', 'using', 'retest')
sys.exit(RES)
