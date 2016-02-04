#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime

from flask import Blueprint, session

from base import util
from etc import config
from base import dao
from base.framework import general, TempResponse, db_conn, form_check, OkResponse, ErrorResponse
from base.decorator import login_required, recognize_device
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base.xform import F_int, F_str, F_datetime
from webcap.logic import shed

task = Blueprint("task", __name__)


@task.route("/task/list/load")
@general("任务列表页面")
@login_required()
@db_conn("db_reader")
@recognize_device()
def task_list_load(db_reader, device_type):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    tasks = dao.get_tasks_by_account_id(db_reader, account_id)
    devices = dao.get_devices_by_account_id(db_reader, account_id)
    return TempResponse(device_type + "/task_list.html", tasks=tasks, devices=devices)


@task.route("/task/device/list")
@general("特定设备任务页面")
@login_required()
@db_conn("db_reader")
@form_check({
    "device_id": F_str("设备ID") & "strict" & "required",
    "device_name": F_str("设备名") & "strict" & "required",
})
@recognize_device()
def device_list(db_reader, safe_vars, device_type):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    tasks = dao.get_tasks_by_account_and_device(db_reader, account_id, safe_vars.device_id)
    devices = dao.get_devices_by_account_id(db_reader, account_id)
    return TempResponse(device_type + "/task_list.html", tasks=tasks, device_name=safe_vars.device_name,
                        device_id=safe_vars.device_id, devices=devices)


@task.route("/task/add/load")
@general("添加任务页面")
@login_required()
@db_conn("db_reader")
@recognize_device()
def task_add_load(db_reader, device_type):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    return TempResponse(device_type + "/task_add.html",
                        task_date=date_select_list(),
                        task_type=const.TYPE.NAME_DICT,
                        devices=dao.get_devices_by_account_id(db_reader, account_id))


def date_select_list():
    d = (u"周日", u"周一", u"周二", u"周三", u"周四", u"周五", u"周六")
    days = []
    for i in xrange(1, config.add_same_task_max_day + 1):
        t = datetime.date.today() + datetime.timedelta(i)
        key = t.strftime('%Y-%m-%d')
        index = int(t.strftime('%w'))
        value = t.strftime('%Y-%m-%d  ') + d[index]
        day = {
            "key": key,
            "value": value,
        }
        days.append(day)
    return days


@task.route("/task/add", methods=["POST"])
@general("添加任务")
@login_required()
@db_conn("db_writer")
@form_check({
    "now": F_int("是否即时") & "strict" & "optional" & (lambda v: (v in const.BOOLEAN.ALL, v)),
    "task_dates": (F_datetime("任务日期", format="%Y-%m-%d") & "strict" & "optional" & "multiple"),
    "execute_time": (F_datetime("执行时间", format='%H:%M')) & "strict" & "optional",
    "duration": (5 <= F_int("持续时间") <= 10) & "strict" & "optional",
    "type": F_int("资源类型") & "strict" & "required" & (lambda v: (v in const.TYPE.ALL, v)),
    "device_id": F_str("设备ID") & "strict" & "required",
})
def task_add(db_writer, safe_vars):
    if safe_vars.device_id == '0':
        return ErrorResponse("请选择设备")
    today = datetime.date.today()
    now = datetime.datetime.now()

    # 检验非即时信息
    if not safe_vars.now:
        if not safe_vars.task_dates:
            return ErrorResponse("任务日期不能为空")
        else:  # 检验任务日期并格式化
            if not safe_vars.execute_time:
                return ErrorResponse("执行时间不能为空")
            raw_dates = set()
            begin = now
            end = now + datetime.timedelta(config.add_same_task_max_day)
            for task_date in safe_vars.task_dates:
                if not (begin <= task_date <= end):
                    return ErrorResponse("任务日期请选择从今天起%d天内的日期" % config.add_same_task_max_day)
                raw_dates.add(task_date.strftime('%Y-%m-%d'))
            if not (0 < len(raw_dates) <= config.add_same_task_max_day):
                return ErrorResponse("任务日期请选择从今天起%d天内的日期" % config.add_same_task_max_day)

            tasks = QS(db_writer).table(T.task).where(
                (F.create_time == list(raw_dates)) & (F.status == const.TASK_STATUS.NORMAL) &
                (F.device_id == safe_vars.device_id)).select()
            if tasks:
                same_days = [t.create_time.strftime('%Y-%m-%d') for t in tasks]
                return ErrorResponse("该设备 %s 有未完成任务,不能再创建任务" % same_days)

    account_id = session[const.SESSION.KEY_ADMIN_ID]
    size = dao.get_account_by_id(db_writer, account_id).size
    if const.ROLE.SIZE[session[const.SESSION.KEY_ROLE_ID]] <= size:
        return ErrorResponse("用户的资源空间有限")

    data = {
        "create_time": today,
        "execute_time": now,
        "duration": safe_vars.duration,
        "now": const.BOOLEAN.TRUE if safe_vars.now else const.BOOLEAN.FALSE,
        "type": safe_vars.type,
        "status": const.TASK_STATUS.NORMAL,
        "account_id": account_id,
        "device_id": safe_vars.device_id,
    }

    # 非即时
    if not safe_vars.now:
        with transaction(db_writer) as trans:
            for task_date in raw_dates:
                data["id"] = util.get_id()
                data["create_time"] = task_date
                data["execute_time"] = safe_vars.execute_time.replace(1970, 1, 1)
                QS(db_writer).table(T.task).insert(data)
            trans.finish()
        return OkResponse()

    # 即时
    if safe_vars.now:
        data["id"] = util.get_id()
        QS(db_writer).table(T.task).insert(data)
        task = dao.get_task_device(db_writer, data["id"])
        shed.do_task(db_writer, task)
    return OkResponse()


@task.route("/task/cancel", methods=["POST"])
@general("任务删除")
@login_required()
@db_conn("db_writer")
@form_check({
    "task_id": F_str("任务ID") & "strict" & "required",
})
def task_cancel(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    with transaction(db_writer) as trans:
        task = dao.update_task_by_account_id(db_writer, account_id, safe_vars.task_id)
        if not task:
            return ErrorResponse("该任务不是你的")
        now = datetime.datetime.now()
        _now = now.replace(year=task.create_time.year,
                           month=task.create_time.month,
                           day=task.create_time.day,
                           hour=task.execute_time.hour,
                           minute=task.execute_time.minute,
                           second=task.execute_time.second)
        if task.status != const.TASK_STATUS.FINISHED and now + datetime.timedelta(
                hours=config.min_hours_left_when_cancel) > _now:
            return ErrorResponse("距离任务开始不足%s小时不能删除" % config.min_hours_left_when_cancel)
        QS(db_writer).table(T.task).where(F.id == safe_vars.task_id).update({
            "status": const.TASK_STATUS.DELETED,
        })
        trans.finish()
    return OkResponse()


@task.route("/task/change/device", methods=["POST"])
@general("改变设备")
@login_required()
@db_conn("db_writer")
@form_check({
    "task_id": F_str("任务ID") & "strict" & "required",
    "device_id": F_str("设备ID") & "strict" & "required",
})
def task_change_device(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]

    with transaction(db_writer) as trans:
        task = dao.update_task_by_account_id(db_writer, account_id, safe_vars.task_id)
        if not task:
            return ErrorResponse("该任务不是你的")
        if task.status == const.TASK_STATUS.FINISHED:
            return ErrorResponse("任务已完成不能修改设备")
        now = datetime.datetime.now()
        _now = now.replace(year=task.create_time.year,
                           month=task.create_time.month,
                           day=task.create_time.day,
                           hour=task.execute_time.hour,
                           minute=task.execute_time.minute,
                           second=task.execute_time.second)

        if now + datetime.timedelta(hours=config.min_hours_left_when_cancel) > _now:
            return ErrorResponse("距离任务开始不足%s小时不能修改设备" % config.min_hours_left_when_cancel)

        QS(db_writer).table(T.task).where(F.id == safe_vars.task_id).update({
            "device_id": safe_vars.device_id,
        })
        trans.finish()
    return OkResponse()
