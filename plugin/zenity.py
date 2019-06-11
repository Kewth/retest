import os

def end_case(typ):
    os.system('zenity --info --text={} 2> /dev/null'.format(typ))

