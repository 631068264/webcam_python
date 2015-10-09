#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

from flask import Blueprint, session

from base.framework import general, TempResponse, db_conn
from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const

task = Blueprint("task", __name__)


@task.route("/task/play/load")
@general("直播页面")
@db_conn("db_reader")
def play_load(db_reader):
    account_id = session[const.SESSION.KEY_ADMIN_ID]
    device = QS(db_reader).table(T.account).where(F.id == account_id).select_one("device").device
    return TempResponse("play_load.html", device=device)
