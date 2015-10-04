#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
from flask import Blueprint, session, redirect

from base import constant as const
from base.framework import general, TempResponse, url_for
from base.logic import login_required

home = Blueprint("home", __name__)


@home.route("/")
@home.route("/index")
@general("主页")
@login_required(const.ROLE.ALL)
def index():
    return TempResponse(const.DEVICE.PC + "/index.html")


@home.route("/login/load")
@general("登录界面")
def login_load():
    if session.get(const.SESSION.KEY_LOGIN):
        return redirect(url_for("home.index"))
    return TempResponse(const.DEVICE.PC + "/login.html")
