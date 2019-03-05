import os

def begin(id_x):
    print('No.{:<4d} '.format(id_x), end='')

def end_case(typ):
    os.system('zenity --info --text={} 2> /dev/null'.format(typ))
    print(' ', typ)

def runtime(use):
    print('run:', use, 'ms', end='')

def exitstatus(ret):
    print('exit:', ret, end='')

def test_ac():
    pass

def test_wa():
    pass

def test_re():
    pass

def test_tle():
    pass

def test_mle():
    pass

def test_ole():
    pass

def test_uke():
    pass

def test_pa():
    pass

def before_judge(problem):
    pass

def start():
    pass

def end(score):
    print('score:', score)
