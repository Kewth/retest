#!/usr/bin/python3
'retest 框架'

import argparse
import os
import sys
from retest import learn
from retest import plugin
from retest import config
from retest import info
from retest import judge
from retest import file_fun

def init_args():
    '初始化参数'
    parser = argparse.ArgumentParser(description='''
A retest command which is like lemon but run in terminal.
And this is the upgraded version of retest
''')
    parser.add_argument('-l', '--learn', action='store_true', \
            help='learn how to use ntest')
    parser.add_argument('-p', '--plugin', action='store_true', \
            help='list all the plugin can be used')
    parser.add_argument('-u', '--use', action='append', \
            help='specify the subconfig')
    return parser.parse_args()

def main():
    '主函数'
    args = init_args()
    if args.learn:
        learn.main()
        return 0
    if args.plugin:
        for i in plugin.list_plugin():
            print(i)
        return 0
    config_dict = config.get_config()
    while config_dict.get('cd'):
        os.chdir(config_dict['cd'])
        config_dict = config.get_config()
    config.upd_config(config_dict, {'plugin': 'default'})
    if config_dict.get('before'):
        os.system(config_dict['before'])
    plugin.get_plugins(config_dict['plugin'])
    if args.use:
        config_dict = config_dict.get(args.use[0])
        if not config_dict:
            info.error_exit('--use: No such a subconfig')
    try:
        plugin.plugin_start()
    except AttributeError as err:
        info.warning('PluginTooOld: {}'.format(err))
    now = 0
    while config_dict.get('T{}'.format(now + 1)):
        now += 1
    file_fun.make_dir()
    if now != 0:
        # 有多个程序待评测
        score = 0
        for i in range(1, now + 1):
            problem = 'T{}'.format(i)
            try:
                plugin.plugin_before_judge(problem)
            except AttributeError as err:
                info.warning('PluginTooOld: {}'.format(err))
            os.makedirs('retest_dir/' + problem)
            sub_config = config_dict[problem]
            for key in config_dict:
                # 用全局配置更新局部配置
                if not sub_config.get(key):
                    sub_config[key] = config_dict[key]
            score += judge.judge(sub_config, './retest_dir/' + problem)
    else:
        try:
            plugin.plugin_before_judge('')
        except AttributeError as err:
            info.warning('PluginTooOld: {}'.format(err))
        score = judge.judge(config_dict, './retest_dir')
    try:
        plugin.plugin_end(score)
    except AttributeError as err:
        info.warning('PluginTooOld: {}'.format(err))
    if config_dict.get('after'):
        os.system(config_dict['after'])
    return 0

if __name__ == '__main__':
    RES = main()
    sys.exit(RES)
