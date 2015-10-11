#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

import threading
import time
import Queue
import datetime

import schedule

from base import constant as const
from etc import config
from base.poolmysql import MySQLdbConnection
from base.smartsql import Table as T, Field as F, QuerySet as QS


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
db = MySQLdbConnection(**config.db_config["db_writer"])


def daily_task():
    date = get_today_range()
    tasks = QS(db).table(T.task).where(
        (F.create_time >= date["start"]) & (F.create_time <= date["end"]) &
        (F.status == const.TASK_STATUS.NORMAL)
    ).order_by("create_time").select(for_update=True)

    for task in tasks:
        device = QS(db).table(T.account).where(F.id == task.account_id).select_one("device").device
        if device:
            schedule.every(task.interval).seconds.do()


def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()


jobqueue = Queue.Queue()

schedule.every().day.at_time("00:00").do(jobqueue.put, daily_task)

worker_thread = threading.Thread(target=worker_main)


def start():
    worker_thread.start()

    while 1:
        schedule.run_pending()
        time.sleep(1)


def get_today_range(today=datetime.date.today()):
    """
    获取一天界限
    :param today:
    :return:
    """
    today_start = today
    today_end = today + datetime.timedelta(1)
    data = {
        "start": today_start,
        "end": today_end,
    }
    return data


def kill(proc):
    """
    关闭子进程
    :param proc:
    :return:
    """
    while True:
        if proc.poll() is not None:
            proc.terminate()
            break


if __name__ == "__main__":
    start()
