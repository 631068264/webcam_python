#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import threading
import time

import schedule


def job(name, j):
    print("I'm running on thread %s" % threading.current_thread() + name)
    print(6 + j)


def run_threaded(func, parm):
    threading.Thread(target=func, args=parm).start()


args = ("123", 6)
kw = {
    "func": job,
    "parm": args,
}
schedule.every(5).seconds.do(run_threaded, **kw)

while 1:
    schedule.run_pending()
    time.sleep(1)

# import time
#
# import schedule
#
#
# def job(message='stuff'):
#     print("I'm working on:", message)
#
#
# schedule.every(10).seconds.do(job, message='things')
#
# if __name__ == "__main__":
#     while 1:
#         schedule.run_pending()
#         time.sleep(1)


# def job():
#     print("I'm running on thread %s" % threading.current_thread())
#
#
# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func)
#     job_thread.start()
#
#
# schedule.every(5).seconds.do(run_threaded, job)
# schedule.every(5).seconds.do(run_threaded, job)
# schedule.every(5).seconds.do(run_threaded, job)
# schedule.every(5).seconds.do(run_threaded, job)
# schedule.every(5).seconds.do(run_threaded, job)
#
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)


#
#
# def job():
#     print("I'm working")
#
#
# def worker_main():
#     while 1:
#         job_func = jobqueue.get()
#         job_func()
#
#
# jobqueue = Queue.Queue()
#
# schedule.every(10).seconds.do(jobqueue.put, job)
# schedule.every(10).seconds.do(jobqueue.put, job)
# schedule.every(10).seconds.do(jobqueue.put, job)
# schedule.every(10).seconds.do(jobqueue.put, job)
# schedule.every(10).seconds.do(jobqueue.put, job)
#
# worker_thread = threading.Thread(target=worker_main)
# worker_thread.start()
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)



import base64
import hashlib
import hmac
import os
import uuid

print(os.path.abspath('..'))  # 查看当前目录的绝对路径
print(os.path.dirname(os.getcwd()))
print(os.getcwd())
print(os.path.split(os.path.realpath(__file__)))

path = os.path.abspath('')

# 正确处理不同操作系统的路径分隔符
dirPath = os.path.join(path, 'dir')  # 路径合并 不用加/
print(dirPath)
if not os.path.exists('../a/b/c/123.tx'):
    os.makedirs('../a/b/c/123.tx')
# os.makedirs('../a/b/c/123.tx')
os.mkdir(dirPath)  # 然后创建一个目录
os.rmdir(dirPath)  # 删掉一个目录:

# 一个路径拆分为两部分，后一部分总是最后级别的目录或文件名
print(os.path.split('/Users/michael/testdir/file.txt'))
# 文件扩展名
print(os.path.splitext('/Users/michael/testdir/file.txt'))
"""
import os
os.path.isfile('test.txt') #如果不存在就返回False
os.path.exists(directory) #如果目录不存在就返回False


# 对文件重命名:
os.rename('xxx.txt', 'test.py')
# 删掉文件:
os.remove('test.py')
"""


# # 列出当前目录下的所有目录
# [x for x in os.listdir('.') if os.path.isdir(x)]
# # 列出所有的.py文件
# [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py']


def md5(content):
    return hashlib.md5(content).hexdigest()


def sha1(content):
    return hashlib.sha1(content).hexdigest()


def b64(content):
    return base64.b64encode(content)


def b32(content):
    return base64.b32encode(content)


def b16(content):
    return base64.b16encode(content)


key = "Hi"


def mac(content):
    return hmac.new("Hi", content).hexdigest()


def uu():
    s = str(uuid.uuid4())
    print(s)
    return s.split('-')

#TODO:uuid - ==> / ==>device
def mm():
    s = str(uuid.uuid4()).split('-')[4]
    print(s)
    m = md5(s)[:13]
    print(m)
    return s + m


print(md5('12'))
print(sha1('12'))
print(b64('12'))
print(b32('12'))
print(b16('12'))
print(mac('12'))
print(uu())
print(mm())
