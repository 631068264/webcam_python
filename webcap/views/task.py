#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime

from flask import Blueprint, session

from base import dao
from base.framework import general, TempResponse, db_conn, form_check, OkResponse, ErrorResponse
from base.logic import login_required
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base.xform import F_int, F_str

task = Blueprint("task", __name__)


# TODO：任务字段有待考虑
@task.route("/task/list/load")
@general("任务列表页面")
@login_required()
@db_conn("db_reader")
def task_set_load(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    tasks = dao.get_tasks_by_account_id(db_reader, account_id)
    return TempResponse("task_list.html", tasks=tasks)


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


@task.route("/task/set")
@general("任务设置")
@login_required()
@db_conn("db_writer")
@form_check({
    "now": F_int("是否即时") & "strict" & "required" & (lambda v: (isinstance(v, bool), v)),
    "duration": F_int("持续时间") & "strict" & "required",
    "interval": F_int("时间间隔") & "strict" & "required",
})
def task_set(db_writer, safe_vars):
    # TODO:时间限制 任务多样性(起始时间，时间多样性) 任务状态是否正在工作
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
            "status": const.TASK_STATUS.NORMAL,
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
            "status": const.TASK_STATUS.DELETED,
        })
        trans.finish()
    return OkResponse()
