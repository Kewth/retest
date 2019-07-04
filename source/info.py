#!/usr/bin/python3
'retest info'

import sys
import shutil
import colorama
from retest import plugin

def print_info(typ, i, use_time=None, exit_status=None):
    '打印 [i] 号测试点信息（类型为 [typ]）'
    try:
        plugin.plugin_begin(i) # No.i
        if typ == 'AC':
            plugin.plugin_test_ac()
        elif typ == 'WA':
            plugin.plugin_test_wa()
        elif typ == 'RE':
            plugin.plugin_test_re()
        elif typ == 'TLE':
            plugin.plugin_test_tle()
        elif typ == 'MLE':
            plugin.plugin_test_mle()
        elif typ == 'OLE':
            plugin.plugin_test_ole()
        elif typ == 'UKE':
            plugin.plugin_test_uke()
        elif typ == 'PA':
            plugin.plugin_test_pa()
        if use_time:
            plugin.plugin_runtime(int(use_time * 1000))
        if exit_status:
            plugin.plugin_exitstatus(exit_status)
        plugin.plugin_end_case(typ)
    except AttributeError as err:
        warning('PluginTooOld: {}'.format(err))

def error_exit(info):
    '打印错误信息并退出'
    print(colorama.Fore.RED, info, \
            colorama.Fore.RESET, file=sys.stderr)
    try:
        shutil.rmtree('retest_dir')
    except FileNotFoundError:
        print(colorama.Fore.RED, 'No retest_dir, exit.', \
                colorama.Fore.RESET, file=sys.stderr)
    sys.exit(1)

def warning(info):
    '打印警告信息'
    print(colorama.Fore.YELLOW, 'Warning: ' + info, \
            colorama.Fore.RESET, file=sys.stderr)
