#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import threading
import time

import schedule


def job(name, j):
    print("I'm running on thread %s" % threading.current_thread() + name)
    print(6 + j)


def run_threaded(job_func=None, arg=None):
    threading.Thread(target=job_func, args=arg).start()


args = ("123", 6)
kw = {
    "job_func": job,
    "arg": args,
}
schedule.every(5).seconds.do(run_threaded, **kw)
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
