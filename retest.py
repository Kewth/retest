#!/usr/bin/python3
# ZHUSHI {{{1
'retest.py'
import os
import threading
# import subprocess
import time
import argparse
# last version : Date:   Wed Oct 31 16:23:36 2018 +0800
VERSION = '5.19'

# print('adasdasdasdsada')
HELPMSG = '''
A retest command which is like lemon but run in terminal.

The first line is the file name:
    e.g.
    (input:) ak
    It will test ak.cpp.

The second line is the data name:
    e.g.
    (input:) data/ak
    It will make dir ./data/da/ as its data dir.

The Third line is some config:
    The config which can be used:
        be= : default=0 : the begining number of test data.
        en= : default=9 : the ending number of test data.
        out= : default=.out : the suffix name of test data.
        time= : default=1 : the time limit of each test whose unit is second.
        o2= : default=0 : If it's set to 1, retest will turn O2 option.
        o3= : default=0 : If it's set to 1, retest will turn O3 option.
'''
PARSER = argparse.ArgumentParser(description=HELPMSG)
PARSER.add_argument('-v', '--version', action='store_true', help='print version')
PARSER.add_argument('-l', '--learn', action='store_true', help='learn something')
PARSER.add_argument('-L', '-lemon', action='store_true', help=
                    'Use lemon\'s directory structure style')
ARGS = PARSER.parse_args()
if ARGS.version:
    print('retest', VERSION)
    print('Made by', 'Kewth')
    exit(0)
if ARGS.learn:
    print(HELPMSG)
    exit(0)

class ThreadRun(threading.Thread): # {{{1
    'Thread to call run'
    def __init__(self, data, name, rid):
        threading.Thread.__init__(self)
        self.data = data
        self.name = name
        self.rid = rid
        self.res = 0
        self.killed = False
    def run(self):
        self.res = run_exe(self.data, self.name, self.rid)
        if self.killed:
            self.res = 2
        else:
            os.system('mv retest_dir'+str(self.rid)+'/'+self.name+'.out own'+str(self.rid)+'.out')
    def kill(self):
        self.killed = True

def run_exe(data, name, _id): # {{{1
    'run the exe'
    os.system('cp '+data+name+str(_id)+'.in retest_dir'+str(_id)+'/'+name+'.in')
    res = os.system('cd retest_dir'+str(_id)+' ; ../own 2> /dev/null < '+name+'.in > '+name+'.out')
    return res // 256

def get_input(): # {{{1
    'get input from stdin'
    In = open('/home/kewth/Kewth_/file.txt', mode='r')
    de_file = In.readline()[:-1]
    de_data = In.readline()[:-1]
    de_more = In.readline()[:-1]
    files = input('enter the file name(default '+de_file+'): ')
    data = input('enter the stdin/out dir name(default '+de_data+'): ')
    more = input('for more config(default '+de_more+'): ')
    In.close()
    if files == '':
        files = de_file
    if data == '':
        data = de_data
    Out = open('/home/kewth/Kewth_/file.txt', mode='w')
    Out.write(files + '\n')
    Out.write(data + '\n')
    res_more, res_str = put_more(more.split(' '), de_more.split(' '))
    Out.write(res_str + '\n')
    Out.close()
    if data[-1] != '/':
        data += '/'
    pos = files.rfind('/')
    if pos == -1:
        name = files
        files = ''
    else:
        name = files[pos+1 : len(files)]
        files = files[0 : pos+1]
    return data, files, name, res_more

def put_dic(dic, more): # {{{1
    'get more and put dict'
    for i in more:
        s = i.split('=')
        if len(s) == 2:
            if s[0] == 'out':
                dic['out'] = s[1]
            elif s[0] == 'ti':
                dic['ti'] = int(s[1])
            elif s[0] == 'be':
                dic['be'] = int(s[1])
            elif s[0] == 'en':
                dic['en'] = int(s[1])
            elif s[0] == 'o2':
                if s[1] == '1':
                    dic['o2'] = 1
                if s[1] == '0':
                    dic['o2'] = 0
            elif s[0] == 'o3':
                if s[1] == '1':
                    dic['o3'] = 1
                if s[1] == '0':
                    dic['o3'] = 0
    return dic

def put_more(more, de_more): # {{{1
    'get more from stdin and return a dict for config'
    dic = {'out': '.out', 'ti': 1, 'be': 0, 'en': 10, 'o2': 0, 'o3': 0, }
    dic = put_dic(dic, de_more)
    dic = put_dic(dic, more)
    res_str = ''
    for i in dic:
        res_str += i + '=' + str(dic[i]) + '  '
    return dic, res_str

def delete_files(ranges): # {{{1
    'delete temporary files'
    for i in ranges:
        os.system('rm own' + str(i) + '.out')
        os.system('rm -r retest_dir'+str(i))
    os.system('rm own')

def create_files(ranges): # {{{1
    'create temporary files'
    for i in ranges:
        os.system('touch 2> /dev/null own' + str(i) + '.out')
        os.system('mkdir -p retest_dir'+str(i))

def Compile(files, name, more):
    'Compile source code'
    g_option = ''
    if more['o2']:
        g_option += ' -O2'
    if more['o3']:
        g_option += ' -O3'
    if name.find('.cpp') != -1:
        name = name[0 : name.find('.cpp')]
    res = os.system('g++ '+files+name+'.cpp -o own ' + g_option)
    return res

def create_thread(data, name, _id, more):
    'create a thread to run the exe'
    thread = ThreadRun(data, name, _id)
    thread.start()
    t_begin = time.time()
    thread.join(more['ti'])
    t_use = time.time() - t_begin
    rm_wa_file = True
    res = thread.res
    if thread.isAlive():
        thread.kill()
        res = -1
    return res, t_use, rm_wa_file

def main(): # {{{1
    'Main fuction'
    print('welcome to use retest ', VERSION)
    allmark = 0
    while True:
        # data, files, num_l, num_r, more = get_input()
        data, files, name, more = get_input()
        if Compile(files, name, more) != 0:
            print('\033[33;40mCompile Error          \033[0m', '')
            return 1
        create_files(range(more['be'], more['en']+1))
        res, mark = 0, 0
        for i in range(more['be'], more['en']+1):
            print(str(i), ' of ', name)
            print('\033[' + str(i - more['be']) + 'B')
            print('\033[2A')
            res, t_use, rm_wa_file = create_thread(data, name, i, more)
            if res == -1:
                print('\033[33;40mTime Limit Exceeded \033[0m')
            elif res == 127 or res == 1:
                print('\033[34;40mFile ERROR          \033[0m')
            elif res == 0:
                os.system('touch WA_' + name + str(i) + '.out')
                command = 'diff -b -B own' + str(i) + '.out ' + data + name + str(i) + more['out']
                diffres = os.system(command + ' > WA_' + name + str(i) + '.out')
                if diffres == 0:
                    print('\033[32;40mAccept              \033[0m', 'time:', '%.4f' % t_use)
                    mark += 100 / (more['en'] - more['be'] + 1)
                else:
                    print('\033[31;40mWrongAnswer         \033[0m')
                    rm_wa_file = False
            else:
                print('\033[31;40mRunTime Error       \033[0m')
            if rm_wa_file:
                os.system('rm WA_' + name + str(i) + '.out 2> /dev/null')
            print('Marks:', '%.2f' % mark)
            print('\033[' + str(4+i-more['be']) + 'A')
        delete_files(range(more['be'], more['en']+1))
        allmark += mark
        print('\033[' + str(4+more['en']-more['be']) + 'B')
        con = input('continue?(y/n)')
        if con == 'n':
            print('All marks: ', allmark)
            return 0

# Begin {{{1
RES = main()
print('Made by Kewth', '(c)')
print('Press', 'Ctrl-c', 'to', 'exit')
exit(RES)

# }}}1
