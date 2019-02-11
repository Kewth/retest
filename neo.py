#!/usr/bin/python3

import sys
import os
import shutil
import argparse
import yaml
import colorama

def read_data(data):
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
            os.system('ln -s ../{}{}{} retest_dir/{}.in'.format( \
                    data, name, '.in', num))
            os.system('ln -s ../{}{}{} retest_dir/{}.ans'.format( \
                    data, name, outname, num))
            res.append(name)
    return res

def error_exit(info):
    print(colorama.Fore.RED, info, colorama.Fore.RESET, file=sys.stderr)
    shutil.rmtree('retest_dir')
    sys.exit(1)

def warning(info):
    print(colorama.Fore.YELLOW, 'Warning: ' + info, \
            colorama.Fore.RESET, file=sys.stderr)

def get_config():
    home_dir = os.path.expandvars('$HOME') + '/.config/retest/'
    config_file = open(home_dir + 'retest.yaml', 'r')
    res = yaml.load(config_file)
    try:
        config_file = open('retest.yaml', 'r')
    except FileNotFoundError:
        error_exit('No retest.yaml was found, input ntest -h to get help')
    current_dict = yaml.load(config_file)
    for key in current_dict:
        res[key] = current_dict[key]
    return res

def print_info(typ):
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

def compile_cpp(name):
    res = os.system('g++ {} -o retest_dir/exe'.format(name))
    if res != 0:
        error_exit('Compile Error')

def judge(num, config):
    timeout = os.system('timeout 0.1 sleep 1')
    print('Judging')
    os.chdir('retest_dir')
    res = 0
    time_limit = config.get('time')
    difftime = config.get('difftime')
    if not time_limit:
        time_limit = 1000
    if not difftime:
        difftime = 1000
    for i in range(1, num):
        print('The {}th judge:'.format(i))
        runres = os.system( \
                'timeout {0} ./exe < {1}.in > {1}.out'.format( \
                time_limit / 100, i))
        if runres == timeout:
            print_info('TLE')
            continue
        elif runres != 0:
            print_info('RE')
            print('exe return {}'.format(runres))
            continue
        diffres = os.system( \
                'timeout {0} icdiff {1}.out {1}.ans > diff{1}'.format( \
                difftime / 1000, i))
        if diffres == timeout:
            warning('Output too long')
            os.system('echo Output too long > diff{}'.format(i))
            diffres = os.system( \
                    'timeout {0} diff {1}.out {1}.ans >> diff{1}'.format( \
                    difftime / 1000, i))
        if diffres == 0:
            print_info('AC')
            res += 100 / num
        elif diffres == timeout:
            print_info('OLE')
        else:
            print_info('WA')
    return int(res)

def make_dir():
    if os.path.exists('retest_dir'):
        shutil.rmtree('retest_dir')
    os.makedirs('retest_dir')

def init_args():
    parser = argparse.ArgumentParser(description='''
A retest command which is like lemon but run in terminal.
And this is the upgraded version of retest
''')
    parser.add_argument('-l', '--learn', action='store_true', \
            help='learn how to use ntest')
    return parser.parse_args()

def learn():
    print('''
How to write retest.yaml?
    The file retest.yaml is used by ntest to judge.
    You can get a full example on ~/.config/retest/example.yaml .

    source:
        The source code you want to judge.

    data:
        The directory where include all data files.

    time:
        The time limit of each judgement.

    difftime:
        The time limit of checking answer.

Some usefull arguments:
    You can rough understanding by using 'ntest -h' or 'ntest --help'.

    --learn, -l:
        Print this message to learn how to use ntest.
        To display this better, you can use 'less' command:
            ntest -l | less
    ''')

def main():
    args = init_args()
    if args.learn:
        learn()
    make_dir()
    config = get_config()
    if not config.get('source'):
        error_exit('No source was read')
    if config.get('filetype') == 'cpp':
        compile_cpp(config['source'])
    else:
        os.system('cp {} retest_dir/exe'.format(config['source']))
    if not config.get('data'):
        error_exit('No data was read')
    files = read_data(config['data'])
    score = judge(len(files), config)
    print('score: {}'.format(score))
    return 0

RES = main()
print('\n\nSee more message in retest_dir\n\n')
print('Made by Kewth', '(c)')
print('Press', 'Ctrl-c', 'to', 'forcefully', 'exit')
print('Thanks', 'for', 'using', 'retest')
sys.exit(RES)
