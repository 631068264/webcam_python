#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime
import shlex
import socket
import subprocess
import os

from apscheduler.schedulers.background import BackgroundScheduler

from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base.framework import db_conn
from base import constant as const


def daily_task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_task, 'cron', hour=0, minute=0, second=0)
    return scheduler


@db_conn("db_writer")
def do_daily_task(db_writer):
    date = get_today_range()
    tasks = QS(db_writer).table(T.task).where(
        (F.create_time >= date["start"]) & (F.create_time <= date["end"]) &
        (F.status == const.TASK_STATUS.NORMAL)
    ).order_by("create_time").select(for_update=True)

    for task in tasks:
        device = QS(db_writer).table(T.account).where(F.id == task.account_id).select_one("device")
        if device != 0 or device is not None:
            scheduler = BackgroundScheduler()
            scheduler.add_job(do_task, 'interval', second=task.interval, args=[device, task, db_writer])
            scheduler.start()


def do_task(device, task, db):
    # TODO: src待定 时间判定 IP在配置里面 src与thumbnail 文件名一致 文件名自动生成
    # TODO: 结合 test/test_seh.py
    ip = socket.gethostbyname(socket.gethostname())
    src = ""
    thumbnail = ""
    video = 'ffmpeg -i rtsp://' + ip + device + '.sdp -c copy -t ' + task.duration + src
    thumb = 'ffmpeg -i rtsp://' + ip + device + '.sdp -f image2 -t 0.001 -s 352x240' + thumbnail

    kill(subprocess.Popen(shlex.split(thumb), shell=True))
    kill(subprocess.Popen(shlex.split(video), shell=True))

    with transaction(db) as trans:
        QS(db).table(T.task).where(F.id == task.id).update({
            "src": src,
            "thumbnail": thumbnail,
            "size": os.path.getsize(src),
        })
        trans.finish()


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
