#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import os
import shlex
import threading
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


def run_thread(job_func, parm):
    threading.Thread(target=job_func, args=parm).start()


def start_daily_task(time):
    schedule.every().days.at(time).do(daily_task)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_task(db, task):
    threading.Thread(target=do_task, args=(db, task)).start()


# TODO：延迟截取 -ss staart_time -c:a -c:v output 为保证质量
# TODO: ffmpeg -i dump.mp4 -ss 20 -t 0.001 -s 380x300 -f image2 xxx.jpg
def daily_task():
    start, end = get_day_range()

    tasks = QS(db).table((T.task__t * T.device__d).on(F.t__device_id == F.d__id)).where(
        (F.d__status == const.DEVICE_STATUS.NORMAL) & (F.t__status == const.TASK.STATUS.NORMAL) &
        (F.t__create_time >= start) & (F.t__create_time <= end)
    ).order_by(F.t__execute_time).select()
    with transaction(db) as trans:
        for task in tasks:
            kw = {
                "job_func": do_task,
                "parm": (db, task),
            }
            schedule.every().day.at(task.execute_time).do(run_thread, **kw)
        trans.finish()


def do_task(db, task):
    # real_device = 'rtsp://218.204.223.237:554/live/1/66251FC11353191F/e7ooqwcfbqjoo80j.sdp'
    real_device = get_real_device(task.device_id)
    path, static_url = get_src_path(task.device_id)
    now = datetime.datetime.now()

    data = {}
    if task.type == const.TASK.TYPE.PHOTOGRAPH:
        data["src_name"] = util.get_file_name('.jpg')
        data["src_path"] = os.path.join(path, data["src_name"])
        cmd = 'ffmpeg -y -i ' + real_device + ' -f image2 -t 0.001 -s 300x380 ' + data["src_path"]
        kill(subprocess.Popen(shlex.split(cmd, posix=False), shell=True))

    if task.type == const.TASK.TYPE.VIDEO:
        data["src_name"] = util.get_file_name('.mp4')
        data["src_path"] = os.path.join(path, data["src_name"])
        cmd = 'ffmpeg -y -i ' + real_device + ' -c:v libx264 -c:a libvo_aacenc -t ' + \
              str(task.duration) + ' ' + data["src_path"]
        kill(subprocess.Popen(shlex.split(cmd, posix=False), shell=True))

    # change_format = 'ffmpeg -y -i ' + src + ' -c:v libx264 -c:a acc ' + src
    size = os.path.getsize(data["src_path"])
    # 更新资源
    QS(db).table(T.src).where(F.id == task.id).insert({
        "create_time": now,
        "src_path": os.path.join(static_url, data["src_name"]),
        # "thumbnail": os.path.join(url, jpg_name),
        "size": size,
        "status": const.SRC_STATUS.NORMAL,
        "type": task.type,
        "device_id": task.device_id,
        "account_id": task.account_id,
    })

    # 更新用户资料
    QS(db).table(T.account).where(F.id == task.account_id).update({
        "size": E("size + %d" % size),
    })

    # 更新任务属性
    task.finish_time = now
    task.status = const.TASK.STATUS.FINISHED
    QS(db).table(T.task).insert(task, on_duplicate_key_update=task)
    return schedule.CancelJob


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


def get_real_device(device_id):
    return const.LOCAL.get_device_src(device_id)


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


def get_day_range(today=None):
    """
    获取一天界限
    :param today:
    :return:
    """
    if today is None:
        today = datetime.date.today()
    today_start = today
    today_end = today + datetime.timedelta(1)

    return today_start, today_end
