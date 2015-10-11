#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

# import threading
# import time
# import schedule
#
#
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

import Queue
import time
import threading

import schedule


def job():
    print("I'm working")


def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()


jobqueue = Queue.Queue()

schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)

worker_thread = threading.Thread(target=worker_main)
worker_thread.start()

while 1:
    schedule.run_pending()
    time.sleep(1)
