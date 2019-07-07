#!/usr/bin/python3
'retest file control'

import shutil
import os
import colorama
from retest import info

def compile_source(name, exe, option, path):
    '''
    将 [name:str] 转换为可执行文件到工作目录的 [exe:str]
    如果是编译，添加参数 [option:str]
    '''
    if not os.path.exists(name):
        info.error_exit('No source file {}, compile error'.format( \
                name))
    if len(name) > 4 and name[-4:] == '.cpp':
        res = os.system( \
                'g++ {} -o {}/{} {}'.format( \
                name, path, exe, option))
    elif len(name) > 2 and name[-2:] == '.c':
        res = os.system( \
                'gcc {} -o {}/{} {}'.format( \
                name, path, exe, option))
    else:
        res = os.system( \
                'cp {0} {1}/{2} ; chmod +x {1}/{2}'.format( \
                name, path, exe))
    if res != 0:
        info.error_exit('Compile Error')

def make_dir(dir_name='retest_dir'):
    '强行创建基目录 [dir_name]'
    if os.path.exists(dir_name):
        info.warning('The directory {} has exist'.format(dir_name))
        files = os.listdir(dir_name)
        for i in files:
            to_remove = '{}/{}'.format(dir_name, i)
            if os.path.isdir(to_remove):
                shutil.rmtree(to_remove)
            else:
                os.remove(to_remove)
        # shutil.rmtree(dir_name)
    else:
        os.makedirs(dir_name)
    if dir_name == 'retest_dir':
        os.system('touch retest_dir/retest.yaml')
        os.system('echo "cd: .." >  retest_dir/retest.yaml')

def make_data(config_dict, path):
    '以 [config_dict] 配置制造数据'
    data = config_dict['data']
    config_dict['data'] = 'dp_data'
    # while os.path.exists(config_dict['data']):
    #     config_dict['data'] += '_'
    from retest import config # 不能全局 import ，原因不详
    config.upd_config(data, {'times': 10}, require=['std', 'rand'])
    make_dir(config_dict['data'])
    compile_source(data['std'], 'std', '', path)
    compile_source(data['rand'], 'rand', '', path)
    for i in range(data['times']):
        print(i + 1, '/', data['times'])
        rand_res = os.system('{}/rand > {}/{}.in 2> /dev/null'.format( \
                path, config_dict['data'], i))
        if rand_res != 0:
            info.error_exit('Make data error: {} exit {}'.format( \
                    data['rand'], rand_res))
        std_res = os.system( \
                '{0}/std < {1}/{2}.in > {1}/{2}.out 2> /dev/null'.format( \
                path, config_dict['data'], i))
        if std_res != 0:
            info.error_exit('Make data error: {} exit {}'.format( \
                    data['std'], std_res))
        print(colorama.Cursor.UP(), end='')

def read_data(data, path):
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
            for j in range(path.count('/')):
                up_path += '/..'
            os.symlink('{}/{}/{}{}'.format( \
                    up_path, data, name, '.in'), '{}/{}.in'.format( \
                    path, num))
            os.symlink('{}/{}/{}{}'.format( \
                    up_path, data, name, outname), '{}/{}.ans'.format( \
                    path, num))
            res.append(name)
    print('cd ..', file=open('{}/retest.yaml'.format(path), 'w'))
    return res
