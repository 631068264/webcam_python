#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import os
import shlex
import socket
import time
import datetime
import subprocess

import schedule

from base import constant as const
from webcap.etc import config
from base.poolmysql import MySQLdbConnection, transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS

db = MySQLdbConnection(**config.db_config["db_writer"])


# TODO:联机调试shed
# TODO:多线程并行
# TODO:大改数据库结构
def daily_task():
    date = get_today_range()
    tasks = QS(db).table((T.task__t * T.account__a).on(F.a__id == F.t__account_id)).where(
        (F.create_time >= date["start"]) & (F.create_time <= date["end"]) & (F.status == const.TASK_STATUS.NORMAL)
    ).order_by("create_time").select("t.*,a.device", for_update=True)

    for task in tasks:
        if task.device and task.device != 0:
            kw = {
                "task": task,
                "db": db,
            }
            schedule.every(task.interval).seconds.do(do_task, **kw)


def get_real_device(device):
    ip = socket.gethostbyname(socket.gethostname())
    return ip + ':554/' + device


def do_task(db, task):
    real_device = get_real_device(task.device)
    path = get_src_path(task.device)
    src = os.path.join(path, 'dump.mp4')
    thumbnail = os.path.join(path, 'dump.jpg')

    video = 'ffmpeg -i rtsp://' + real_device + '.sdp -c copy -t ' + task.duration + ' ' + src
    thumb = 'ffmpeg -i rtsp://' + real_device + '.sdp -f image2 -t 0.001 -s 352x240 ' + thumbnail

    kill(subprocess.Popen(shlex.split(thumb), shell=True))
    kill(subprocess.Popen(shlex.split(video), shell=True))

    with transaction(db) as trans:
        QS(db).table(T.task).where(F.id == task.id).update({
            "src": src,
            "thumbnail": thumbnail,
            "size": os.path.getsize(src),
        })
        trans.finish()


def start():
    schedule.every().day.at_time("00:00").do(daily_task)
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


def get_src_path(device):
    """
    创建个人目录
    :param device:
    :return:
    """
    root_path = os.path.dirname(os.path.dirname(os.getcwd()))
    download_path = os.path.join(root_path, "download")
    personal_path = os.path.join(download_path, device)

    if not os.path.exists(personal_path):
        os.makedirs(personal_path)

    return personal_path


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
