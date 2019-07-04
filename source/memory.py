#!/usr/bin/python3
'retest memory'

import os
import resource

def mem_out():
    'MLE 的返回值'
    limit_memory(1)
    res = os.system('echo "Neo Retest !" > /dev/null')
    limit_memory(-1)
    return res

def limit_memory(maxsize):
    '限制子进程运行内存 [maxsize] 字节（ -1 表示无限制）'
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))
