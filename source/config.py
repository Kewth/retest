#!/usr/bin/python3
'retest config'

import yaml
import xdg.BaseDirectory as XDG
from retest import info
from retest import file_fun

def get_config():
    '''
    获取配置信息
    返回一个字典
    '''
    # 获取全局配置
    try:
        config_file = open(XDG.xdg_data_home + '/retest/retest.yaml', 'r')
    except FileNotFoundError:
        info.error_exit( \
                ('No global retest.yaml was found in ' + \
                '{}/retest/, ' + \
                'input retest -l to get help').format(XDG.xdg_data_home))
    global_config = yaml.load(config_file, Loader=yaml.FullLoader)
    # 获取当前配置
    try:
        config_file = open('retest.yaml', 'r')
    except FileNotFoundError:
        info.error_exit( \
                'No retest.yaml was found, ' + \
                'input retest -l to get help')
    current_config = yaml.load(config_file, Loader=yaml.FullLoader)
    # 用全局配置更新局部配置
    if not global_config:
        info.warning('Global config file is empty!')
        global_config = {}
    if not current_config:
        info.warning('Config file is empty!')
        current_config = {}
    upd_config(current_config, global_config)
    return current_config

def upd_config(config_dict, default, require=[]):
    '''
    用 [default] 配置更新 [config_dict] 配置
    [require] 为必须的配置列表
    '''
    for key in default:
        if not config_dict.get(key):
            config_dict[key] = default[key]
    for key in require:
        if not config_dict.get(key):
            info.error_exit('No {} was read'.format(key))

def check_config(config_dict, path):
    '检查配置字典 [config_dict] 的合法性'
    upd_config(config_dict, { \
            'time': 1000, 'difftime': 1000, 'plugin': 'default', \
            'spj': XDG.xdg_data_home + '/retest/spj', 'option': '', 'memory': 512}, \
            require=['source', 'data'])
    if config_dict['data'].__class__ is dict:
        file_fun.make_data(config_dict, path)
    # 在工作目录制造 spj 与 exe
    file_fun.compile_source(config_dict['spj'], 'spj', '', path)
    file_fun.compile_source(config_dict['source'], 'exe', config_dict['option'], path)

if __name__ == '__main__':
    print(get_config())
