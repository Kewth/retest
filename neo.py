#!/usr/bin/python3
'新的 retest'

import sys
import os
import shutil
import argparse
import time
import yaml
import colorama

PATH = './retest_dir'
TIMEOUT = os.system('(timeout 0.1 sleep 1) 2>/dev/null')
HOME_DIR = os.path.expandvars('$HOME') + '/.config/retest/'

# Plugin {{{
sys.path.append(HOME_DIR + 'plugin/')
try:
    import _print
except ImportError as err:
    print(colorama.Fore.RED, 'Plugin Error:', err, \
            colorama.Fore.RESET, file=sys.stderr)
    sys.exit(1)
# }}}

# Print {{{
def print_info(typ, i, use_time=None, exit_status=None):
    '打印 [i] 号测试点信息（类型为 [typ]）'
    _print.begin(i) # No.i
    if typ == 'AC':
        _print.test_ac()
    elif typ == 'WA':
        _print.test_wa()
    elif typ == 'RE':
        _print.test_re()
    elif typ == 'TLE':
        _print.test_tle()
    elif typ == 'OLE':
        _print.test_ole()
    elif typ == 'UKE':
        _print.test_uke()
    elif typ == 'PA':
        _print.test_pa()
    if use_time:
        _print.runtime(int(use_time * 1000))
    if exit_status:
        _print.exitstatus(exit_status)
    print()

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

# }}}

# Config {{{
def get_config():
    '''
    获取配置信息
    返回一个字典
    '''
    config_file = open(HOME_DIR + 'retest.yaml', 'r')
    global_config = yaml.load(config_file)
    try:
        config_file = open('retest.yaml', 'r')
    except FileNotFoundError:
        error_exit( \
                'No retest.yaml was found, input ntest -l to get help')
    current_config = yaml.load(config_file)
    # 用全局配置更新局部配置
    upd_config(current_config, global_config)
    return current_config

def upd_config(config, default, require=[]):
    '''
    用 [default] 配置更新 [config] 配置
    [require] 为必须的配置列表
    '''
    for key in default:
        if not config.get(key):
            config[key] = default[key]
    for key in require:
        if not config.get(key):
            error_exit('No {} was read'.format(require[key]))

def check_config(config):
    '检查配置字典 [config] 的合法性'
    upd_config(config, { \
            'time': 1000, 'difftime': 1000, \
            'spj': '~/.config/retest/spj', 'option': ''}, \
            require=['source', 'data'])
    if config['data'].__class__ is dict:
        make_data(config)
    # 在工作目录制造 spj 与 exe
    compile_source(config['spj'], 'spj', '')
    compile_source(config['source'], 'exe', config['option'])

# }}}

# File {{{
def compile_source(name, exe, option):
    '将 [name] 转换为可执行文件到工作目录的 [exe]'
    if len(name) > 4 and name[-4:] == '.cpp':
        res = os.system( \
                'g++ {} -o {}/{} {}'.format(name, PATH, exe, option))
    elif len(name) > 2 and name[-2:] == '.c':
        res = os.system( \
                'gcc {} -o {}/{} {}'.format(name, PATH, exe, option))
    else:
        res = os.system( \
                'cp {0} {1}/{2} ; chmod +x {1}/{2}'.format( \
                name, PATH, exe))
    if res != 0:
        error_exit('Compile Error')

def make_dir(dir_name='retest_dir'):
    '强行创建基目录 [dir_name]'
    if os.path.exists(dir_name):
        warning('The directory {} has exist'.format(dir_name))
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

def make_data(config, times=100):
    '以 [config] 配置制造数据'
    data = config['data']
    config['data'] = 'dp_data'
    # while os.path.exists(config['data']):
    #     config['data'] += '_'
    upd_config(data, {'times': 10}, require=['std', 'rand'])
    make_dir(config['data'])
    compile_source(data['std'], 'std', '')
    compile_source(data['rand'], 'rand', '')
    for i in range(data['times']):
        print(i + 1, '/', data['times'])
        rand_res = os.system('{}/rand > {}/{}.in'.format( \
                PATH, config['data'], i))
        if rand_res != 0:
            error_exit('Make data error: {} exit {}'.format( \
                    data['rand'], rand_res))
        std_res = os.system( \
                '{0}/std < {1}/{2}.in > {1}/{2}.out'.format( \
                PATH, config['data'], i))
        if std_res != 0:
            error_exit('Make data error: {} exit {}'.format( \
                    data['std'], std_res))
        print(colorama.Cursor.UP(), end='')

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

# }}}

# Argument {{{
def init_args():
    '初始化参数'
    parser = argparse.ArgumentParser(description='''
A retest command which is like lemon but run in terminal.
And this is the upgraded version of retest
''')
    parser.add_argument('-l', '--learn', action='store_true', \
            help='learn how to use ntest')
    parser.add_argument('-u', '--use', action='append', \
            help='specify the subconfig')
    return parser.parse_args()

# }}}

# Learn {{{
def learn():
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
        The time limit of checking answer(running spj).
        Its unit is millisecond.
        It's set to 1000 by default.

    input:
        The file where exe get input.
        It's set to standard input by default.

    output:
        The file where exe get output.
        It's set to standard output by default.

    spj:
        The Special Judge File (Lemon Style).
        If it's set to ~ (null), ntest will judge traditionally.
        It's set to ~ by default

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

# Judge {{{
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
            input_str = ''
        else:
            input_str = ' < {}.in '.format(i)
        if config.get('output'):
            os.system('ln -sf {}.out {}'.format( \
                    i, config['output']))
            output_str = ''
        else:
            output_str = ' > {}.out '.format(i)
        begin_time = time.time()
        runres = os.system( \
			'''
                echo 'timeout {} ./exe {}{} 2> res{} 2>/dev/null' | bash 2>/dev/null
		'''.format( \
                config['time'] / 1000, input_str, output_str, i))
        use_time = time.time() - begin_time
        # 程序超时（没有输出）
        if runres == TIMEOUT:
            print_info('TLE', i)
            continue
        # 程序运行时错误（没有输出）
        elif runres != 0:
            print_info('RE', i, exit_status=runres)
            continue
        score = 100 / (num - 1)
        get = check_ans_spj(config, i, score)
        # 正确
        if get == score:
            print_info('AC', i, use_time=use_time)
            print('Accept', file=open('res{}'.format(i), 'w'))
        # 错误
        elif get == 0:
            print_info('WA', i, use_time=use_time)
        # 部分正确
        else:
            print_info('PA', i, use_time=use_time)
        res += get
    for i in range(PATH.count('/')):
        os.chdir('..')
    return int(res)

# }}}

# Main {{{
def main():
    '主函数'
    args = init_args()
    if args.learn:
        learn()
        return 0
    config = get_config()
    if args.use:
        config = config.get(args.use[0])
        if not config:
            error_exit('--use: No such a subconfig')
    _print.start()
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
            _print.before_judge(problem)
            os.makedirs('retest_dir/' + problem)
            sub_config = config[problem]
            for key in config:
                # 用全局配置更新局部配置
                if not sub_config.get(key):
                    sub_config[key] = config[key]
            score += judge(sub_config)
    else:
        _print.before_judge('')
        score = judge(config)
    _print.end(score)
    return 0

RES = main()
sys.exit(RES)

# }}}
