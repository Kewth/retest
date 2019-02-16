'打印测试点信息'

def begin(id_x):
    '测 [id_x] 号测试点前'
    print('No.{:<4d} '.format(id_x), end='')

def runtime(use):
    '运行时间 [use] ms'
    print('RunTime:', use, 'ms', end='')

def exitstatus(ret):
    'RE 返回 [ret]'
    print('Exit status:', ret, end='')
