#!/usr/bin/python3
'retes judge'

import os
import time
from retest import info
from retest import file_fun
from retest import memory
from retest import config
TIMEOUT = os.system('(timeout 0.1 sleep 1) 2>/dev/null')

def check_ans_spj(config_dict, i, score):
    '''
    在工作目录用 spj 进行测试（测试点编号为 [i] ）
    以 [config_dict] 为配置
    返回得分
    '''
    if not os.path.exists('sp.log'):
        os.mknod('sp.log')
    spres = os.system( \
            'timeout {2} ./spj \
            {0}.in {0}.out {0}.ans {1} sp.get sp.log'.format( \
            i, score, config_dict['difftime']))
    # 评分过程超时
    if spres == TIMEOUT:
        info.print_info('OLE', i)
        print('Output too long', file=open('res{}'.format(i), 'a'))
    # 评分过程错误
    elif spres != 0:
        info.print_info('UKE', i)
    try:
        get = float(open('sp.get', 'r').readline()[:-1])
    except FileNotFoundError:
        info.error_exit('Spj doesn\'t output score')
    print('\nMessage from spj:', file=open('res{}'.format(i), 'a'))
    os.system('cat sp.log >> res{}'.format(i))
    return get

def judge(config_dict, path):
    '''
    评测一道题目，以 [config_dict] 为配置
    返回该题目的分数
    '''
    config.check_config(config_dict, path)
    files = file_fun.read_data(config_dict['data'], path)
    num = len(files)
    if num == 1:
        info.warning('No input and output file.')
    res = 0
    os.chdir(path)
    for i in range(1, num):
        # 评测单个测试点
        if config_dict.get('input'):
            if os.path.exists(config_dict['input']):
                os.remove(config_dict['input'])
            os.symlink('{}.in'.format(i), config_dict['input'])
            input_str = ''
        else:
            input_str = ' < {}.in '.format(i)
        if config_dict.get('output'):
            if os.path.exists(config_dict['output']):
                os.remove(config_dict['output'])
            os.symlink('{}.out'.format(i), config_dict['output'])
            output_str = ''
        else:
            output_str = ' > {}.out '.format(i)
        begin_time = time.time()
        try:
            memory.limit_memory(config_dict['memory'] * 1024 * 1024)
            runres = os.system( \
                            '''
                    echo 'timeout {} ./exe {}{} 2> res{}' \
                    | bash 2>/dev/null
                    '''.format( \
                    config_dict['time'] / 1000, input_str, output_str, i))
        except MemoryError:
            runres = memory.mem_out()
        memory.limit_memory(-1)
        use_time = time.time() - begin_time
        # 程序超时（ 被 kill ）
        if runres == TIMEOUT:
            info.print_info('TLE', i)
            continue
        # 程序内存超出限制（ 被 kill ）
        elif runres == memory.mem_out():
            info.print_info('MLE', i)
            continue
        # 程序运行时错误（ 被 kill ）
        elif runres != 0:
            if runres % 256 == 0:
                runres >>= 8
            info.print_info('RE', i, exit_status=runres)
            continue
        score = 100 / (num - 1)
        get = check_ans_spj(config_dict, i, score)
        # 正确
        if get == score:
            print('Accept', file=open('res{}'.format(i), 'w'))
            info.print_info('AC', i, use_time=use_time)
        # 错误
        elif get == 0:
            info.print_info('WA', i, use_time=use_time)
        # 部分正确
        else:
            info.print_info('PA', i, use_time=use_time)
        res += get
    for i in range(path.count('/')):
        os.chdir('..')
    return int(res + 0.5)
