'简易输出'

def begin(id_x):
    print('No.{:<4d} '.format(id_x), end='')

def end_case(typ):
    print(typ)

def runtime(use):
    print('run:', use, 'ms', end='')

def exitstatus(ret):
    print('exit:', ret, end='')

