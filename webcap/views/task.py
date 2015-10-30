#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime

from flask import Blueprint, session

from etc import config
from base import dao
from base.framework import general, TempResponse, db_conn, form_check, OkResponse, ErrorResponse
from base.logic import login_required
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base.xform import F_int, F_str, F_datetime

task = Blueprint("task", __name__)


@task.route("/task/list/load")
@general("任务列表页面")
@login_required()
@db_conn("db_reader")
def task_list_load(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    tasks = dao.get_tasks_by_account_id(db_reader, account_id)
    return TempResponse("task_list.html", tasks=tasks)


@task.route("/task/add/load")
@general("添加任务页面")
@login_required()
def task_add_load():
    return TempResponse("task_add.html", task_date=date_select_list(), task_type=const.TASK.TYPE.NAME_DICT)


def date_select_list():
    d = (u"周日", u"周一", u"周二", u"周三", u"周四", u"周五", u"周六")
    days = {}
    for i in xrange(0, config.add_same_task_max_day):
        t = datetime.date.today() + datetime.timedelta(i)
        key = t.strftime('%Y-%m-%d')
        index = int(t.strftime('%w'))
        value = t.strftime('%Y-%m-%d') + d[index]
        if i == 0:
            value += u'（今天）'
        days[key] = value
    return days


@task.route("/task/add", methods=["POST"])
@general("添加任务")
@login_required()
@db_conn("db_writer")
@form_check({
    "task_date": (F_datetime("任务日期", format="%Y-%m-%d") & "strict" & "required" & "multiple"),
    "execute_time": (F_datetime("执行时间", format='%H:%M')) & "strict" & "required",
    "duration": F_int("持续时间") & "strict" & "required",
    "interval": F_int("时间间隔") & "strict" & "required",
    "now": F_int("是否即时") & "strict" & "required" & (lambda v: (isinstance(v, bool), v)),
    "type": F_int("资源类型") & "strict" & "required" & (lambda v: (v in const.TASK.TYPE.ALL, v)),
})
def task_add(db_writer, safe_vars):
    # TODO:即时就只有今天 不用填执行时间 非即时检验任务日期
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    size = dao.get_account_by_id(db_writer, account_id).size
    if const.ROLE.SIZE[session[const.SESSION.KEY_ROLE_ID]] <= size:
        return ErrorResponse("用户的资源空间有限")

    with transaction(db_writer) as trans:
        QS(db_writer).table(T.task).insert({
            "create_time": datetime.date.today(),
            "duration": safe_vars.duration,
            "interval": safe_vars.interval,
            "now": const.IS_NOW.NOW if safe_vars.now else const.IS_NOW.NOT_NOW,
            "account_id": account_id,
            "status": const.TASK.STATUS.NORMAL,
        })
        trans.finish()
    return OkResponse()


@task.route("/task/cancel")
@general("任务删除")
@login_required()
@db_conn("db_writer")
@form_check({
    "task_id": F_int("任务ID") & "strict" & "required",
})
def task_cancel(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    task = dao.update_task_by_account_id(db_writer, account_id, safe_vars.task_id)
    if not task:
        return ErrorResponse("该任务不是你的")

    with transaction(db_writer) as trans:
        QS(db_writer).table(T.task).where(F.id == safe_vars.task_id).update({
            "status": const.TASK.STATUS.DELETED,
        })
        trans.finish()
    return OkResponse()


@task.route("/task/device/list")
@general("特定设备任务页面")
@login_required()
@db_conn("db_reader")
@form_check({
    "device_id": F_str("设备ID") & "strict" & "required",
    "device_name": F_str("设备名") & "strict" & "required",
})
def device_list(db_reader, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    tasks = dao.get_tasks_by_account_and_device(db_reader, account_id, safe_vars.device_id)
    return TempResponse("task_device_list.html", tasks=tasks, device_name=safe_vars.device_name,
                        device_id=safe_vars.device_id)
