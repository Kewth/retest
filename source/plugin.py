#!/usr/bin/python3
'retest plugin'

import os
import sys
import xdg.BaseDirectory as XDG
from retest import info

def list_plugin():
    '返回所有可用的插件'
    files = os.listdir('{}/retest/plugin/'.format(XDG.xdg_data_home))
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
        info.error_exit('No plugin named {}.\nTry retest -p'.format(name))
    length = len(get_plugin.plugins)
    os.system( \
            'cp {}/retest/plugin/{}.py /tmp/ntest_plugin{}.py'.format( \
            XDG.xdg_data_home, name, length))
    sys.path.append('/tmp')
    if length == 0:
        import ntest_plugin0
        get_plugin.plugins.append(ntest_plugin0)
    elif length == 1:
        import ntest_plugin1
        get_plugin.plugins.append(ntest_plugin1)
    elif length == 2:
        import ntest_plugin2
        get_plugin.plugins.append(ntest_plugin2)
    elif length == 3:
        import ntest_plugin3
        get_plugin.plugins.append(ntest_plugin3)
    elif length == 4:
        import ntest_plugin4
        get_plugin.plugins.append(ntest_plugin4)
    elif length == 5:
        import ntest_plugin5
        get_plugin.plugins.append(ntest_plugin5)
    elif length == 6:
        import ntest_plugin6
        get_plugin.plugins.append(ntest_plugin6)
    elif length == 7:
        import ntest_plugin7
        get_plugin.plugins.append(ntest_plugin7)
    elif length == 8:
        import ntest_plugin8
        get_plugin.plugins.append(ntest_plugin8)
    elif length == 9:
        import ntest_plugin9
        get_plugin.plugins.append(ntest_plugin9)
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
            except AttributeError:
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
def plugin_exitstatus(plugin, args):
    plugin.exitstatus(args[0])

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
    plugin.before_judge(args[0])

@search_plugin
def plugin_start(plugin, args):
    plugin.start()

@search_plugin
def plugin_end(plugin, args):
    plugin.end(args[0])

if __name__ == '__main__':
    print(list_plugin())
