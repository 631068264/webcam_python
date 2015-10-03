#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
from flask import Blueprint

from base.framework import TempResponse, general

test = Blueprint("test", __name__)


@test.route("/test/rtsp")
@general("rstp播放测试")
def rstp():
    return TempResponse("test/play.html")
