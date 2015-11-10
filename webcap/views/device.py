#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

from flask import Blueprint, session

from base import dao, util
from base.framework import general, TempResponse, db_conn, form_check, OkResponse, ErrorResponse
from base.logic import login_required
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, Expr as E, QuerySet as QS
from base import constant as const
from base.xform import F_str

device = Blueprint("device", __name__)


# TODO:设备封禁
@device.route("/device/list/load")
@general("设备列表页面")
@login_required()
@db_conn("db_reader")
def device_list_load(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    devices = dao.get_devices_by_account_id(db_reader, account_id)
    return TempResponse("device_list.html", devices=devices)


@device.route("/device/add", methods=['POST'])
@general("设备设置")
@login_required()
@db_conn("db_writer")
@form_check({
    "device_name": F_str("设备名") & "strict" & "required",
})
def device_add(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]

    device_num = dao.get_account_by_id(db_writer, account_id).device_num
    if device_num >= const.ROLE.DEVICE[session[const.SESSION.KEY_ROLE_ID]]:
        return ErrorResponse("用户设备过多,不能再增加")

    with transaction(db_writer) as trans:
        QS(db_writer).table(T.device).insert({
            "id": util.get_device(),
            "name": safe_vars.device_name,
            "status": const.DEVICE_STATUS.NORMAL,
            "account_id": account_id,
        })

        QS(db_writer).table(T.account).where(F.id == account_id).update({
            "device_num": E("device_num + 1"),
        })

        trans.finish()
    return OkResponse()


@device.route("/device/edit")
@general("设备改名")
@login_required()
@db_conn("db_writer")
@form_check({
    "device_id": F_str("设备ID") & "strict" & "required",
    "device_name": F_str("设备名") & "strict" & "required",
})
def device_edit(db_writer, safe_vars):
    with transaction(db_writer)as trans:
        device = dao.update_device_by_account_id(db_writer, session[const.SESSION.KEY_ADMIN_ID], safe_vars.device_id)
        if not device:
            return ErrorResponse("没有权限修改该设备")
        device.name = safe_vars.device_name

        QS(db_writer).table(T.device).update(device)
        trans.finish()
    return OkResponse()


@device.route("/device/cancel")
@general("设备删除")
@login_required()
@db_conn("db_writer")
@form_check({
    "device_id": F_str("设备ID") & "strict" & "required",
})
def device_cancel(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    with transaction(db_writer) as trans:
        device = dao.update_device_by_account_id(db_writer, account_id, safe_vars.device_id)
        if not device:
            return ErrorResponse("该设备不是你的")

        QS(db_writer).table(T.device).where(F.id == device.id).update({
            "status": const.DEVICE_STATUS.DELETED,
        })
        # TODO: 资源暂时不分设备
        QS(db_writer).table(T.task).where(F.device_id == device.id).update({
            "status": const.TASK_STATUS.DELETED,
        })

        QS(db_writer).table(T.account).where(F.id == account_id).update({
            "device_num": E("if(device_num - 1 < 0, 0 ,device_num - 1)"),
        })
        trans.finish()
    return OkResponse()


@device.route("/device/play")
@general("直播页面")
@login_required()
@db_conn("db_reader")
@form_check({
    "device_id": F_str("设备ID") & "strict" & "required",
})
def device_play(db_reader, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    device = dao.get_device_by_account_id(db_reader, account_id, safe_vars.device_id)
    if not device:
        return ErrorResponse("还没有申请设备")
    device_src = const.LOCAL.get_device_src(device.id)
    return TempResponse("play_load.html", device=device, device_src=device_src)
