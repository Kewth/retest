import os

def begin(id_x):
    begin.last = id_x

def end_case(typ):
    if typ == 'AC':
        os.system('rm {0}.in {0}.out {0}.ans res{0}'.format(begin.last))
