#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import urlparse
import datetime
from flask import Blueprint, request, session

from base import constant as const
from base import dblogic as dbl
from base import util
from base.framework import json_check, form_check, general, db_conn
from base.poolmysql import transaction
from base.framework import DjJsonResponse, login_required
from base.smartsql import Table as T, Field as F, Expr as E, QuerySet as QS
from base.xform import F_str, F_mobile, F_int
from etc import config as cfg


my = Blueprint("my", __name__)


@my.route("/api/test", methods=["GET"])
@general("test")
@db_conn("db_reader")
def test(db_reader):
    params = {
        "message": u"未实现",
    }
    return DjJsonResponse(const.STATUS.FAIL, **params)
