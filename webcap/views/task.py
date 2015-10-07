#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime
import shlex
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler

from base.smartsql import Table as T, Field as F, QuerySet as QS
from base.framework import db_conn


def daily_task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_task, 'cron', hour=0, minute=0, second=0)
    return scheduler


@db_conn("db_writer")
def do_daily_task(db_writer):
    date = get_today_range()
    tasks = QS(db_writer).table(T.task).where(
        (F.create_time >= date["start"]) & (F.create_time <= date["end"])).order_by("create_time").select(
        for_update=True)
    for task in tasks:
        device = QS(db_writer).table(T.account).where(F.id == task.account_id).select_one("device")
        if device != 0 or device is not None:
            do_task(device, task, db_writer)
            # TODO:清楚redis remove_all_job()
            scheduler = BackgroundScheduler()
            # scheduler.add_jobstore('redis', jobs_key=task.id, run_times_key=task.account_id)
            scheduler.add_job(do_task, 'interval', second=task.interval, args=[device, task, db_writer])
            scheduler.start()


def do_task(device, task, db):
    # TODO: IP 和 src待定 时间判定 video 大小
    ip = ""
    src = ""
    thumbnail = ""
    video = 'ffmpeg -i rtsp://' + ip + device + '.sdp -c copy -t ' + task.duration + src
    thumb = 'ffmpeg -i rtsp://' + ip + device + '.sdp -f image2 -t 0.001 -s 352x240' + thumbnail

    subprocess.Popen(shlex.split(video), shell=True)
    subprocess.Popen(shlex.split(thumb), shell=True)

    QS(db).table(T.task).where(F.id == task.id).update({
        "src": src,
        "thumbnail": thumbnail,
        "size": "",
    })


def get_today_range(today=datetime.date.today()):
    today_start = today
    today_end = today + datetime.timedelta(1)
    data = {
        "start": today_start,
        "end": today_end,
    }
    return data
