#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime

from flask import Blueprint, session

from base.framework import general, TempResponse, db_conn, form_check, OkResponse
from base.logic import login_required
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base.xform import F_int
from base.xform import F_str

task = Blueprint("task", __name__)


@task.route("/task/play")
@general("直播页面")
@login_required()
@db_conn("db_reader")
def play(db_reader):
    # TODO:页面修改参数 美化 设备识别码不能过长
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    device = QS(db_reader).table(T.account).where(F.id == account_id).select_one("device").device
    return TempResponse("play_load.html", device=device)


@task.route("/task/set/load")
@general("任务设置页面")
@login_required()
@db_conn("db_reader")
def task_set_load(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    tasks = QS(db_reader).table(T.task).where(F.account_id == account_id).order_by(F.create_time, desc=True).select()
    return TempResponse("task_set.html", tasks=tasks)


@task.route("/task/set")
@general("任务设置")
@login_required()
@db_conn("db_writer")
@form_check({
    "name": F_str("任务名") & "optional",
    "duration": F_int("持续时间") & "strict" & "required",
    "interval": F_int("时间间隔") & "strict" & "required",
})
def task_set(db_writer, safe_vars):
    # TODO:时间限制 用户size的限制 任务与资源路径分表
    QS(db_writer).table(T.task).insert({
        "name": safe_vars.name,
        "create_time": datetime.date.today(),
        "duration": safe_vars.duration,
        "interval": safe_vars.interval,
        "account_id": session[const.SESSION.KEY_ADMIN_ID],
        "status": const.TASK_STATUS.NORMAL,
    })
    return OkResponse()


@task.route("/task/src/list")
@general("资源列表")
@login_required()
@db_conn("db_reader")
def src_list(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    # TODO:新增字段完成时间
    tasks = QS(db_reader).table(T.task).where(F.account_id == account_id).order_by(F.finish_time, desc=True).select()
    return TempResponse("src_list.html", tasks=tasks)
