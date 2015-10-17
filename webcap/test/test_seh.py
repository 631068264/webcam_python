#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import os
import shlex
import time
import datetime
import subprocess

import schedule

from base import smartpool
from base import constant as const
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS



# db = MySQLdbConnection(**config.db_config["db_writer"])
db = smartpool.ConnectionProxy("db_writer")

# TODO:多线程并行
# TODO:video速度超级慢
def daily_task():
    date = get_today_range()
    tasks = QS(db).table((T.task__t * T.account__a).on(F.a__id == F.t__account_id)).where(
        (F.t__create_time >= date["start"]) & (F.t__create_time <= date["end"]) & (
            F.t__status == const.TASK_STATUS.NORMAL)
    ).order_by("create_time").select("t.*,a.device", for_update=True)

    for task in tasks:
        if task.device and task.device != 0:
            kw = {
                "task": task,
                "db": db,
            }
            schedule.every(task.interval).seconds.do(do_task, **kw)


def get_real_device(device):
    return const.LOCAL.IP + device + const.LOCAL.SUFFIX


def do_task(db, task):
    real_device = 'rtsp://218.204.223.237:554/live/1/66251FC11353191F/e7ooqwcfbqjoo80j.sdp'
    path = get_src_path(task.device)
    src = os.path.join(path, 'dump.mp4')
    thumbnail = os.path.join(path, 'dump.jpg')

    video = 'ffmpeg -y -i ' + real_device + ' -c copy -t ' + str(task.duration) + ' ' + src
    thumb = 'ffmpeg -y -i ' + real_device + ' -f image2 -t 0.001 -s 352x240 ' + thumbnail

    kill(subprocess.Popen(shlex.split(thumb, posix=False), shell=True))
    kill(subprocess.Popen(shlex.split(video, posix=False), shell=True))

    with transaction(db) as trans:
        QS(db).table(T.task).where(F.id == task.id).update({
            "src": src,
            "thumbnail": thumbnail,
            "size": os.path.getsize(src),
        })
        trans.finish()


def start():
    schedule.every().day.at("10:46").do(daily_task)
    while 1:
        schedule.run_pending()
        time.sleep(1)


def get_today_range(today=None):
    """
    获取一天界限
    :param today:
    :return:
    """
    if today is None:
        today = datetime.date.today()
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
