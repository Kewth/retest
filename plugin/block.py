import colorama

def begin(id_x):
    pass

def end_case(typ):
    pass

def runtime(use):
    pass

def exitstatus(ret):
    pass

def test_ac():
    print('{} {}'.format(colorama.Back.GREEN, colorama.Back.RESET), end='')

def test_wa():
    print('{} {}'.format(colorama.Back.RED, colorama.Back.RESET), end='')

def test_re():
    print('{} {}'.format(colorama.Back.MAGENTA, colorama.Back.RESET), end='')

def test_tle():
    print('{} {}'.format(colorama.Back.YELLOW, colorama.Back.RESET), end='')

def test_ole():
    print('{} {}'.format(colorama.Back.WHITE, colorama.Back.RESET), end='')

def test_uke():
    print('{} {}'.format(colorama.Back.BLUE, colorama.Back.RESET), end='')

def test_pa():
    print('{}x{}'.format(colorama.Back.GREEN, colorama.Back.RESET), end='')

def before_judge(problem):
    pass

def start():
    pass

def end(score):
    print()
