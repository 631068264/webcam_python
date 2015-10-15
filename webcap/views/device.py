#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

from flask import Blueprint, session

from base import dao, util
from base.framework import general, TempResponse, db_conn, form_check, OkResponse, ErrorResponse
from base.logic import login_required
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base.xform import F_int, F_str

device = Blueprint("device", __name__)


@device.route("/device/list/load")
@general("设备列表页面")
@login_required()
@db_conn("db_reader")
def device_list_load(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    devices = dao.get_device_by_account_id(db_reader, account_id)
    return TempResponse("device_list.html", devices=devices)


@device.route("/device/set")
@general("设备设置")
@login_required()
@db_conn("db_writer")
@form_check({
    "name": F_str("设备名") & "strict" & "required",
})
def device_set(db_writer, safe_vars):
    # TODO:设备个数限制
    account_id = session[const.SESSION.KEY_ADMIN_ID]

    with transaction(db_writer) as trans:
        QS(db_writer).table(T.device).insert({
            "id": util.get_device(),
            "name": safe_vars.name,
            "status": const.DEVICE_STATUS.NORMAL,
            "account_id": account_id,
        })
        trans.finish()
    return OkResponse()


@device.route("/device/cancel")
@general("设备删除")
@login_required()
@db_conn("db_writer")
@form_check({
    "device_id": F_int("设备ID") & "strict" & "required",
})
def device_cancel(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    device = dao.update_device_by_account_id(db_writer, account_id, safe_vars.device_id)
    if not device:
        return ErrorResponse("该任务不是你的")

    with transaction(db_writer) as trans:
        QS(db_writer).table(T.device).where(F.id == safe_vars.device_id).update({
            "status": const.DEVICE_STATUS.DELETED,
        })
        trans.finish()
    return OkResponse()
