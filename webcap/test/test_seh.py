#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import os
import shlex
import time
import datetime
import subprocess

import schedule

from etc import config
from base import smartpool
from base import util
from base import constant as const
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, Expr as E, QuerySet as QS

db = smartpool.ConnectionProxy("db_writer")


# TODO:video速度超级慢
# TODO:video保存在static下 保存 download\\0d0b0e608af645a0590d0c425\\3967ee185b844ec5825d2cea9903b2f9.mp4
# TODO:video 转格式
# TODO：video 花屏
def daily_task():
    date = get_today_range()
    # 检验设备合法性
    tasks = QS(db).table((T.task__t * T.device__d).on(F.t__device_id == F.d__id)).where(
        (F.d__status == const.DEVICE_STATUS.NORMAL) & (F.t__status == const.TASK_STATUS.NORMAL) & (
            F.t__create_time >= date["start"]) & (F.t__create_time <= date["end"])
    ).order_by("t.create_time").select(for_update=True)

    # TODO:多线程并行 线程池
    for task in tasks:
        kw = {
            "task": task,
            "db": db,
        }
        # TODO：可能只做一遍 interval为空
        schedule.every(task.interval).seconds.do(do_task, **kw)


def get_real_device(device_id):
    return const.LOCAL.get_device_src(device_id)


def do_task(db, task):
    real_device = 'rtsp://218.204.223.237:554/live/1/66251FC11353191F/e7ooqwcfbqjoo80j.sdp'
    # real_device = get_real_device(task.device_id)
    path, url = get_src_path(task.device_id)

    mp4_name = util.get_file_name('.mp4')
    jpg_name = util.get_file_name('.jpg')

    src = os.path.join(path, mp4_name)
    thumbnail = os.path.join(path, jpg_name)

    video = 'ffmpeg -y -i ' + real_device + ' -c copy -t ' + str(task.duration) + ' ' + src
    thumb = 'ffmpeg -y -i ' + real_device + ' -f image2 -t 0.001 -s 352x240 ' + thumbnail
    change_format = 'ffmpeg -y -i ' + src + ' -c:v libx264 -c:a acc ' + src

    kill(subprocess.Popen(shlex.split(thumb, posix=False), shell=True))
    kill(subprocess.Popen(shlex.split(video, posix=False), shell=True))
    kill(subprocess.Popen(shlex.split(change_format, posix=False), shell=True))

    size = os.path.getsize(src)
    with transaction(db) as trans:
        QS(db).table(T.src).where(F.id == task.id).insert({
            "create_time": datetime.datetime.now(),
            "src_path": os.path.join(url, mp4_name),
            "thumbnail": os.path.join(url, jpg_name),
            "size": size,
            "device_id": task.device_id,
            "account_id": task.account_id,
        })
        # TODO:用户size限制 怎么停
        QS(db).table(T.account).where(F.id == task.account_id).update({
            "size": E("size + %d" % size),
        })
        trans.finish()


def start(task_time):
    schedule.every().day.at(task_time).do(daily_task)
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


def get_src_path(device_id):
    """
    创建个人目录
    :param device_id:
    :return:
    """
    root_path = os.path.dirname(os.getcwd())
    save_root_path = os.path.join("webcap", config.static_path.replace('/', '') + os.sep + "download")
    download_path = os.path.join(root_path, save_root_path)
    device_path = os.path.join(download_path, device_id)
    url_path = os.path.join(os.path.join(config.static_path, "download"), device_id).replace('\\', '/')
    if not os.path.exists(device_path):
        os.makedirs(device_path)

    return device_path, url_path


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
