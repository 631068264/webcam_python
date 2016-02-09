#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

from flask import Blueprint, session

from base import dao
from base.framework import general, TempResponse, db_conn, form_check, OkResponse, ErrorResponse
from base.decorator import login_required, recognize_device
from base.poolmysql import transaction
from base.smartsql import Table as T, Field as F, Expr as E, QuerySet as QS
from base import constant as const
from base.xform import F_str

src = Blueprint("src", __name__)


@src.route("/src/list/load")
@general("资源列表")
@login_required()
@db_conn("db_reader")
@recognize_device()
@form_check({
    "type": F_str("请求类型") & "optional",
})
def src_list(db_reader, safe_vars, device_type):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    srcs = None
    video_srcs = None
    photo_srcs = None
    if device_type == const.DEVICE.PC:
        srcs = dao.get_srcs_by_account_id(db_reader, account_id)
    elif device_type == const.DEVICE.APP:
        video_srcs = dao.get_video_srcs(db_reader, account_id, const.TYPE.VIDEO)
        photo_srcs = dao.get_video_srcs(db_reader, account_id, const.TYPE.PHOTOGRAPH)
    templ_name = "/src_list.html"
    if safe_vars.type == const.BLOCK.BLOCK:
        templ_name = "/src_list_block.html"
    return TempResponse(device_type + templ_name,
                        srcs=srcs,
                        video_srcs=video_srcs,
                        photo_srcs=photo_srcs)


# TODO：回收站封禁
@src.route("/src/cancel", methods=["POST"])
@general("资源删除")
@login_required()
@db_conn("db_writer")
@form_check({
    "src_id": F_str("资源ID") & "strict" & "required",
})
def src_cancel(db_writer, safe_vars):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    with transaction(db_writer) as trans:
        src = dao.update_src_by_account_id(db_writer, account_id, safe_vars.src_id)
        if not src:
            return ErrorResponse("该资源不是你的")

        QS(db_writer).table(T.src).where(F.id == safe_vars.src_id).update({
            "status": const.SRC_STATUS.DELETED,
        })

        QS(db_writer).table(T.account).where(F.id == account_id).update({
            "size": E("IF((size - %d ) < 0,0,size - %d)" % src.size),
        })
        trans.finish()
    return OkResponse()
