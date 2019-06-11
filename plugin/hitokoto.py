# By ld_liaomo
'在看一言的时候还可以改题哦'
import os
import urllib.request

def before_judge(problem):
    print('先来条骚话')
    os.system('fortune')

def end(score):
    hitokoto = 'https://v1.hitokoto.cn?encode=text&charset=utf-8'
    print('\n这是不知道为什么要写在这里的一言……\n')
    print(urllib.request.urlopen(hitokoto).readline().decode('utf-8'))
