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
def list_plugin():
    '返回所有可用的插件'
    files = os.listdir('{}plugin/'.format(HOME_DIR))
    plugins = []
    for i in files:
        if len(i) >= 3 and i[-3:] == '.py':
            plugins.append(i[:-3])
    return plugins

def get_plugin(name):
    '''
    获取插件 [name] 到全局变量 PRINT :-)
    变量 plugins 为已用的插件
    '''
    if name not in list_plugin():
        error_exit('No plugin named {}.\nTry ntest -p'.format(name))
    os.system( \
            'cp {0}plugin/{1} /tmp/ntest_plugin.py'.format( \
            HOME_DIR, name + '.py'))
    sys.path.append('/tmp')
    import ntest_plugin
    get_plugin.plugins.append(ntest_plugin)
get_plugin.plugins = []

def get_plugins(plugins):
    '获取插件'
    if type(plugins) is not list:
        plugins = [plugins]
    for i in plugins:
        get_plugin(i)

def search_plugin(pluginrun):
    '插件接口的模板'
    def res(*args):
        for i in get_plugin.plugins:
            try:
                pluginrun(i, args)
            except AttributeError as err:
                pass
    return res

# 以下都是插件接口
@search_plugin
def plugin_begin(plugin, args):
    plugin.begin(args[0])

@search_plugin
def plugin_end_case(plugin, args):
    plugin.end_case(args[0])

@search_plugin
def plugin_runtime(plugin, args):
    plugin.runtime(args[0])

@search_plugin
def plugin_exitsatus(plugin, args):
    plugin.exitsatus(args[0])

@search_plugin
def plugin_test_ac(plugin, args):
    plugin.test_ac()

@search_plugin
def plugin_test_wa(plugin, args):
    plugin.test_wa()

@search_plugin
def plugin_test_re(plugin, args):
    plugin.test_re()

@search_plugin
def plugin_test_tle(plugin, args):
    plugin.test_tle()

@search_plugin
def plugin_test_mle(plugin, args):
    plugin.test_mle()

@search_plugin
def plugin_test_ole(plugin, args):
    plugin.test_ole()

@search_plugin
def plugin_test_uke(plugin, args):
    plugin.test_uke()

@search_plugin
def plugin_test_pa(plugin, args):
    plugin.test_pa()

@search_plugin
def plugin_before_judge(plugin, args):
    plugin.exitsatus(args[0])

@search_plugin
def plugin_start(plugin, args):
    plugin.start()

@search_plugin
def plugin_end(plugin, args):
    plugin.end(args[0])

# }}}

# Memory {{{
def mem_out():
    'MLE 的返回值'
    limit_memory(1)
    res = os.system('echo "Neo Retest !" > /dev/null')
    limit_memory(-1)
    return res

def limit_memory(maxsize):
    '限制子进程运行内存 [maxsize] 字节（ -1 表示无限制）'
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

# }}}

# Print {{{
def print_info(typ, i, use_time=None, exit_status=None):
    '打印 [i] 号测试点信息（类型为 [typ]）'
    try:
        plugin_begin(i) # No.i
        if typ == 'AC':
            plugin_test_ac()
        elif typ == 'WA':
            plugin_test_wa()
        elif typ == 'RE':
            plugin_test_re()
        elif typ == 'TLE':
            plugin_test_tle()
        elif typ == 'MLE':
            plugin_test_mle()
        elif typ == 'OLE':
            plugin_test_ole()
        elif typ == 'UKE':
            plugin_test_uke()
        elif typ == 'PA':
            plugin_test_pa()
        if use_time:
            plugin_runtime(int(use_time * 1000))
        if exit_status:
            plugin_exitstatus(exit_status)
        plugin_end_case(typ)
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

# }}}

# Config {{{
def get_config():
    '''
    获取配置信息
    返回一个字典
    '''
    # 获取全局配置
    try:
        config_file = open(HOME_DIR + 'retest.yaml', 'r')
    except FileNotFoundError:
        error_exit( \
                'No global retest.yaml was found in \
                ~/.config/retest/, \
                input ntest -l to get help')
    global_config = yaml.load(config_file, Loader=yaml.FullLoader)
    # 获取当前配置
    try:
        config_file = open('retest.yaml', 'r')
    except FileNotFoundError:
        error_exit( \
                'No retest.yaml was found, \
                input ntest -l to get help')
    current_config = yaml.load(config_file, Loader=yaml.FullLoader)
    # 用全局配置更新局部配置
    if not global_config:
        warning('Global config file is empty!')
        global_config = {}
    if not current_config:
        warning('Config file is empty!')
        current_config = {}
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
            error_exit('No {} was read'.format(key))

def check_config(config):
    '检查配置字典 [config] 的合法性'
    upd_config(config, { \
            'time': 1000, 'difftime': 1000, 'plugin': '_print', \
            'spj': HOME_DIR + 'spj', 'option': '', 'memory': 512}, \
            require=['source', 'data'])
    if config['data'].__class__ is dict:
        make_data(config)
    # 在工作目录制造 spj 与 exe
    compile_source(config['spj'], 'spj', '')
    compile_source(config['source'], 'exe', config['option'])

# }}}

# File {{{
def compile_source(name, exe, option):
    '''
    将 [name:str] 转换为可执行文件到工作目录的 [exe:str]
    如果是编译，添加参数 [option:str]
    '''
    if not os.path.exists(name):
        error_exit('No source file {}, compile error'.format( \
                name))
    if len(name) > 4 and name[-4:] == '.cpp':
        res = os.system( \
                'g++ {} -o {}/{} {}'.format( \
                name, PATH, exe, option))
    elif len(name) > 2 and name[-2:] == '.c':
        res = os.system( \
                'gcc {} -o {}/{} {}'.format( \
                name, PATH, exe, option))
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

def make_data(config):
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
        rand_res = os.system('{}/rand > {}/{}.in 2> /dev/null'.format( \
                PATH, config['data'], i))
        if rand_res != 0:
            error_exit('Make data error: {} exit {}'.format( \
                    data['rand'], rand_res))
        std_res = os.system( \
                '{0}/std < {1}/{2}.in > {1}/{2}.out 2> /dev/null'.format( \
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
            os.symlink('{}/{}/{}{}'.format( \
                    up_path, data, name, '.in'), '{}/{}.in'.format( \
                    PATH, num))
            os.symlink('{}/{}/{}{}'.format( \
                    up_path, data, name, outname), '{}/{}.ans'.format( \
                    PATH, num))
            res.append(name)
    os.system('touch {}/retest.yaml'.format(PATH))
    os.system('echo "cd: .." >  {}/retest.yaml'.format(PATH))
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
    parser.add_argument('-p', '--plugin', action='store_true', \
            help='list all the plugin can be used')
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

        If a sub dict was given, ntest will make data itself:
            rand: (required)
                The file which make input file.

            std: (required)
                The file which make output file.

            times: (required)
                The number of the test-cases.

    time:
        The time limit of each judgement.
        Its unit is millisecond.
        It's set to 1000 by default.

    memory:
        The memory limit of each judgement.
        Its unit is megabyte.
        NOTE: MLE won't be displayed somtimes (it'll be shown as RE).

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
        The Special Judge File (Lemon Style[1]).
        If it's set to ~ (null), ntest will judge traditionally.
        It's set to ~ by default

    option:
        The option to compile (only used for g++ and gcc).
        Many Oier may want to open O2 switch. Just add 'option: -O2'.

    cd:
        The directory where the real retest.yaml is.
        Of course is's set to './' by default.

    before:
        The command you want to run before ntest.

    after:
        The command you want to run after ntest.
        For example, if the data directory is too lagre that is in the .rar file, just add this:
            before: rar x *.rar data
            after: rm -r data

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

    --plugin, -p:
        Print all plugins you can use.

    --use, -u:
        Use subconfig of retest.yaml.

    [1]: Lemon Style
        The spj is given 6 arguments.
        Argv[1] is the input file.
        Argv[2] is the output file of user.
        Argv[3] is the answer file.
        Argv[4] is the a number which means max scores of the test-case.
        Argv[5] is the output file of spj which include the scores user get.
        Argv[6] is the log file of spj.
    ''')

# }}}

# Judge {{{
def check_ans_spj(config, i, score):
    '''
    在工作目录用 spj 进行测试（测试点编号为 [i] ）
    以 [config] 为配置
    返回得分
    '''
    if not os.path.exists('sp.log'):
        os.mknod('sp.log')
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
    try:
        get = float(open('sp.get', 'r').readline()[:-1])
    except FileNotFoundError:
        error_exit('Spj doesn\'t output score')
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
    if num == 1:
        warning('No input and output file.')
    res = 0
    os.chdir(PATH)
    for i in range(1, num):
        # 评测单个测试点
        if config.get('input'):
            if os.path.exists(config['input']):
                os.remove(config['input'])
            os.symlink('{}.in'.format(i), config['input'])
            input_str = ''
        else:
            input_str = ' < {}.in '.format(i)
        if config.get('output'):
            if os.path.exists(config['output']):
                os.remove(config['output'])
            os.symlink('{}.out'.format(i), config['output'])
            output_str = ''
        else:
            output_str = ' > {}.out '.format(i)
        begin_time = time.time()
        try:
            limit_memory(config['memory'] * 1024 * 1024)
            runres = os.system( \
                            '''
                    echo 'timeout {} ./exe {}{} 2> res{}' \
                    | bash 2>/dev/null
                    '''.format( \
                    config['time'] / 1000, input_str, output_str, i))
        except MemoryError:
            runres = mem_out()
        limit_memory(-1)
        use_time = time.time() - begin_time
        # 程序超时（ 被 kill ）
        if runres == TIMEOUT:
            print_info('TLE', i)
            continue
        # 程序内存超出限制（ 被 kill ）
        elif runres == mem_out():
            print_info('MLE', i)
            continue
        # 程序运行时错误（ 被 kill ）
        elif runres != 0:
            if runres % 256 == 0:
                runres >>= 8
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
    return int(res + 0.5)

# }}}

# Main {{{
def main():
    '主函数'
    args = init_args()
    if args.learn:
        learn()
        return 0
    if args.plugin:
        for i in list_plugin():
            print(i)
        return 0
    config = get_config()
    while config.get('cd'):
        os.chdir(config['cd'])
        config = get_config()
    if config.get('before'):
        os.system(config['before'])
    get_plugins(config['plugin'])
    if args.use:
        config = config.get(args.use[0])
        if not config:
            error_exit('--use: No such a subconfig')
    try:
        plugin_start()
    except AttributeError as err:
        warning('PluginTooOld: {}'.format(err))
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
            try:
                plugin_before_judge(problem)
            except AttributeError as err:
                warning('PluginTooOld: {}'.format(err))
            os.makedirs('retest_dir/' + problem)
            sub_config = config[problem]
            for key in config:
                # 用全局配置更新局部配置
                if not sub_config.get(key):
                    sub_config[key] = config[key]
            score += judge(sub_config)
    else:
        try:
            plugin_before_judge('')
        except AttributeError as err:
            warning('PluginTooOld: {}'.format(err))
        score = judge(config)
    try:
        plugin_end(score)
    except AttributeError as err:
        warning('PluginTooOld: {}'.format(err))
    if config.get('after'):
        os.system(config['after'])
    return 0

RES = main()
sys.exit(RES)

# }}}
