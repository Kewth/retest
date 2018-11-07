#!/usr/bin/python3
# ZHUSHI {{{1
'retest.py'
import os
import threading
# import subprocess
import time
import argparse
import multiprocessing
import psutil
# last version : Date:   Wed Oct 31 16:23:36 2018 +0800
VERSION = '6.35'
CONFIG_FILE = os.path.expandvars('$HOME')+'/.config/retest/file.txt'
LOCK_BEGIN = multiprocessing.Lock()

LEARNMSG = '''
The first line is the file name:
    e.g.
    (input:) ak
    It will test ak.cpp.

The second line is the data name:
    e.g.
    (input:) data/ak
    It will make dir ./data/da/ as its data dir.

The Third line is some configuration:
    The config which can be used:
        be= : default=0 : the begining number of test data.
        en= : default=9 : the ending number of test data.
        out= : default=.out : the suffix name of test data.
        ti= : default=1000 : the time limit of each test whose unit is millisecond.
        me= : default=512 : the memory limit of each test whose unit is megabyte.
        o2= : default=0 : If it's set to 1, retest will turn O2 option.
        o3= : default=0 : If it's set to 1, retest will turn O3 option.

Some usefull arguments:
    You can rough understanding by using 'retest -h' or 'retest --help'.

    --version, -v:
            Print version message like this:
                retest VERSION
                Made by Kewth
    --learn, -l:
            Print this message.
            To display this better, you can use 'less' command:
                retest -l | less
    --default, -d:
            Use the last configuration instead of input.
            If you're judge your code again and again, this arguments can help
        you not to press enter three times.
    --lemon, -L USERNAME/FILENAME:
            !!Make sure your working directory is in the root directory of
        lemon which has data/ and source/, otherwise it won't work will!!
            Use lemon\' s directory structure instead of input.
            For example, if your name in source directory is IAKIOI, and the
        problem you want ot judge is ak, just input:
                retest -L IAKIOI/ak
            Then input above configuration.
'''

HELPMSG = '''
A retest command which is like lemon but run in terminal.
'''
PARSER = argparse.ArgumentParser(description=HELPMSG)
PARSER.add_argument('-v', '--version', action='store_true', help='print version')
PARSER.add_argument('-l', '--learn', action='store_true', help='learn something')
PARSER.add_argument('-d', '--default', action='store_true', help=
                    'Use default config (like press enter three times)')
PARSER.add_argument('-L', '--lemon', action='append', help=
                    'Use lemon\'s directory structure style '
                    + '(Followed by the user name and file name)')
PARSER.add_argument('-p', '--process', action='store_true', help=
                    'Use process instead of thread to get memroy or '
                    + 'other information but it is not safe enough '
                    + 'even it will throw error sometimes')
ARGS = PARSER.parse_args()
if ARGS.version:
    print('retest', VERSION)
    print('Made by', 'Kewth')
    exit(0)
if ARGS.learn:
    print(LEARNMSG)
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
            os.system('mv retest_dir'+str(self.rid)+'/'+self.name+'.out own_of_retest'+str(self.rid)+'.out')
    def kill(self):
        self.killed = True

class ProcessRun(multiprocessing.Process): # {{{1
    'Process to call run'
    def __init__(self, data, fname, rid, connect):
        multiprocessing.Process.__init__(self)
        self.data = data
        self.fname = fname
        self.rid = rid
        self.killed = False
        self.connect = connect
    def run(self):
        exitres = run_exe(self.data, self.fname, self.rid)
        if self.killed:
            exitres = 2
        else:
            os.system('mv retest_dir'+str(self.rid)+'/'+self.fname+'.out own_of_retest'+str(self.rid)+'.out')
        self.connect.send(exitres)
        self.connect.close()
    def kill(self):
        self.killed = True
        self.terminate()
        self.join()
        os.system('pkill own_of_retest')

def run_exe(data, name, _id): # {{{1
    'run the exe'
    LOCK_BEGIN.acquire()
    os.system('cp '+data+name+str(_id)+'.in retest_dir'+str(_id)+'/'+name+'.in')
    res = os.system('cd retest_dir'+str(_id)+' ; ../own_of_retest 2> /dev/null < '+name+'.in > '+name+'.out')
    return res // 256

def get_input(): # {{{1
    'get input from stdin'
    In = open(CONFIG_FILE, mode='r')
    de_file = In.readline()[:-1]
    de_data = In.readline()[:-1]
    de_more = In.readline()[:-1]
    files = ''
    data = ''
    more = ''
    if ARGS.default:
        print('You\'re using default configuration')
        files = de_file
        data = de_data
    elif ARGS.lemon:
        get = ARGS.lemon[0]
        pos = get.find('/')
        files = 'source/' + get
        data = 'data/' + get[pos: ]
        os.system('echo the files: ; ls ' + data)
        more = input('for more config(default '+de_more+'): ')
    else:
        files = input('enter the file name(default '+de_file+'): ')
        data = input('enter the stdin/out dir name(default '+de_data+'): ')
        if files == '':
            files = de_file
        if data == '':
            data = de_data
        os.system('echo the files: ; ls ' + data)
        more = input('for more config(default '+de_more+'): ')
    In.close()
    Out = open(CONFIG_FILE, mode='w')
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
            elif s[0] == 'me':
                dic['me'] = int(s[1])
    return dic

def put_more(more, de_more): # {{{1
    'get more from stdin and return a dict for config'
    dic = {'out': '.out', 'ti': 1000, 'be': 0, 'en': 10, 'o2': 0, 'o3': 0, 'me': 512}
    dic = put_dic(dic, de_more)
    dic = put_dic(dic, more)
    res_str = ''
    for i in dic:
        res_str += i + '=' + str(dic[i]) + '  '
    return dic, res_str

def delete_files(ranges): # {{{1
    'delete temporary files'
    for i in ranges:
        os.system('rm own_of_retest' + str(i) + '.out')
        os.system('rm -r retest_dir'+str(i))
    os.system('rm own_of_retest')

def create_files(ranges): # {{{1
    'create temporary files'
    for i in ranges:
        os.system('touch 2> /dev/null own_of_retest' + str(i) + '.out')
        os.system('mkdir -p retest_dir'+str(i))

def Compile(files, name, more): # {{{1
    'Compile source code'
    g_option = ''
    if more['o2']:
        g_option += ' -O2'
    if more['o3']:
        g_option += ' -O3'
    if name.find('.cpp') != -1:
        name = name[0 : name.find('.cpp')]
    res = os.system('g++ '+files+name+'.cpp -o own_of_retest ' + g_option)
    return res

def create_process(data, name, _id, more): # {{{1
    'create a process to run the exe'
    pr_con, son_con = multiprocessing.Pipe()
    LOCK_BEGIN.acquire()
    proc = ProcessRun(data, name, _id, son_con)
    proc.start()
    t_use, mem_use, res = -0.001, -1024*1024, 0
    max_t = more['ti']/1000
    memory_limit = more['me']*1024*1024
    exe_pro = psutil.Process(proc.pid)
    t_begin = time.time()
    LOCK_BEGIN.release()
    while proc.is_alive() and exe_pro.is_running():
        child, exe_dict = exe_pro.children(), {}
        if exe_pro.is_running():
            exe_dict['cmdline'] = exe_pro.cmdline()
            # exe_dict = exe_pro.as_dict()
        else:
            break
        if exe_dict['cmdline'] == [] or exe_dict['cmdline'][0][0] == '.':
            break
        if child == []:
            proc.join(0.00001)
            continue
        else:
            exe_pro = child[0]
    while proc.is_alive() and exe_pro.is_running():
        info = exe_pro.memory_info()
        mem_use = max(mem_use, info.rss, info.vms, info.shared, info.text, info.data)
        if mem_use > memory_limit:
            res = -2
            break
        t_use = time.time() - t_begin
        if t_use > max_t:
            res = -1
            break
        time.sleep(0.004)
    proc.join(0.100)
    rm_wa_file = True
    if res < 0:
        proc.kill()
    else:
        res = pr_con.recv()
    LOCK_BEGIN.release()
    return res, int(t_use*1000), int(mem_use/1024/1024), rm_wa_file

def create_thread(data, name, _id, more): # {{{1
    'create a thread to run the exe'
    thread = ThreadRun(data, name, _id)
    thread.start()
    t_begin = time.time()
    thread.join(more['ti']/1000)
    t_use = time.time() - t_begin
    rm_wa_file = True
    res = thread.res
    if thread.isAlive():
        thread.kill()
        res = -1
    LOCK_BEGIN.release()
    return res, int(t_use*1000), -1, rm_wa_file

def main(): # {{{1
    'Main fuction'
    print('welcome to use retest ', VERSION)
    data, files, name, more = get_input()
    if Compile(files, name, more) != 0:
        print('\033[33;40mCompile Error          \033[0m', '')
        return 1
    create_files(range(more['be'], more['en']+1))
    res, score = 0, 0
    for i in range(more['be'], more['en']+1):
        print(str(i), ' of ', name)
        print('\033[' + str((i-more['be'])*2) + 'B')
        print('\033[2A')
        res, t_use, mem_use, rm_wa_file = None, None, None, None
        if ARGS.process:
            res, t_use, mem_use, rm_wa_file = create_process(data, name, i, more)
        else:
            res, t_use, mem_use, rm_wa_file = create_thread(data, name, i, more)
        if res == -1:
            print('\033[33;40mTime Limit Exceed   \033[0m')
            print('-> time: INF, memory:', mem_use, 'MB')
        elif res == -2:
            print('\033[33;40mMemory Limit Exceed \033[0m')
            print('-> time: XXX, memory: INF')
        elif res == 127 or res == 1:
            print('\033[34;40mFile ERROR          \033[0m')
            print('-> time: XXX, memory: XXX')
        elif res == 0:
            os.system('touch WA_' + name + str(i) + '.out')
            command = 'diff -b -B own_of_retest' + str(i) + '.out ' + data + name + str(i) + more['out']
            diffres = os.system(command + ' > WA_' + name + str(i) + '.out')
            if diffres == 0:
                print('\033[32;40mAccept              \033[0m')
                print('-> time:', t_use, 'ms, memory:', mem_use, 'MB')
                score += 100 / (more['en'] - more['be'] + 1)
            else:
                print('\033[31;40mWrongAnswer         \033[0m')
                print('-> time:', t_use, 'ms, memory:', mem_use, 'MB')
                rm_wa_file = False
        else:
            print('\033[35;40mRunTime Error       \033[0m')
            print('-> time: XXX, memory: XXX')
        if rm_wa_file:
            os.system('rm WA_' + name + str(i) + '.out 2> /dev/null')
        print('Scores:', '%.2f' % score)
        print('\033[' + str(3+(i-more['be']+1)*2) + 'A')
    delete_files(range(more['be'], more['en']+1))
    print('\033[' + str(4+(more['en']-more['be'])*2) + 'B')
    return 0

# Begin {{{1
RES = main()
print('Made by Kewth', '(c)')
print('Press', 'Ctrl-c', 'to', 'forcefully', 'exit')
print('Thanks', 'for', 'using', 'retest')
exit(RES)

# }}}1
