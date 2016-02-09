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


def daily_task():
    date = get_today_range()
    # 检验设备合法性
    tasks = QS(db).table((T.task__t * T.device__d).on(F.t__device_id == F.d__id)).where(
        (F.d__status == const.DEVICE_STATUS.NORMAL) & (F.t__status == const.TASK_STATUS.NORMAL) & (
            F.t__create_time >= date["start"]) & (F.t__create_time <= date["end"])
    ).order_by("t.create_time").select(for_update=True)

    for task in tasks:
        kw = {
            "task": task,
            "db": db,
        }
        schedule.every(task.interval).seconds.do(do_task, **kw)


def get_real_device(device_id):
    return util.get_device_src(device_id)


def do_task(db, task):
    # real_device = 'rtsp://218.204.223.237:554/live/1/66251FC11353191F/e7ooqwcfbqjoo80j.sdp'
    real_device = get_real_device(task.device_id)
    path, static_url = get_src_path(task.device_id)
    now = datetime.datetime.now()

    data = {}
    if task.type == const.TYPE.PHOTOGRAPH:
        data["src_name"] = util.get_file_name('.jpg')
        data["src_path"] = os.path.join(path, data["src_name"])
        cmd = 'ffmpeg -y -i ' + real_device + ' -f image2 -t 0.001 -s 300x380 ' + data["src_path"]
        kill(subprocess.Popen(shlex.split(cmd, posix=False), shell=True))

    if task.type == const.TYPE.VIDEO:
        data["src_name"] = util.get_file_name('.mp4')
        data["src_path"] = os.path.join(path, data["src_name"])
        cmd = 'ffmpeg -y -i ' + real_device + ' -c:v libx264 -c:a libvo_aacenc -t ' + \
              str(task.duration) + ' ' + data["src_path"]
        kill(subprocess.Popen(shlex.split(cmd, posix=False), shell=True))

    # change_format = 'ffmpeg -y -i ' + src + ' -c:v libx264 -c:a acc ' + src

    size = os.path.getsize(data["src_path"])
    with transaction(db) as trans:
        # 更新资源
        QS(db).table(T.src).where(F.id == task.id).insert({
            "create_time": now,
            "src_path": os.path.join(static_url, data["src_name"]),
            # "thumbnail": os.path.join(url, jpg_name),
            "size": size,
            "status": const.SRC_STATUS.NORMAL,
            "device_id": task.device_id,
            "account_id": task.account_id,
        })

        # 更新用户资料
        QS(db).table(T.account).where(F.id == task.account_id).update({
            "size": E("size + %d" % size),
        })

        # 更新任务属性
        task.finish_time = now
        TASK_STATUS = const.TASK_STATUS.FINISHED
        QS(db).table(T.task).insert(task, on_duplicate_key_update=task)
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


def kill(proc, kill_time=None):
    """
    关闭子进程
    :param proc:
    :return:
    """
    if kill_time is None:
        while True:
            if proc.poll() is not None:
                proc.terminate()
                break
    else:
        time.sleep(kill_time)
        proc.terminate()


if __name__ == "__main__":
    start()
