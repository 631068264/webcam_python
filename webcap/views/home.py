#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import random

from captcha.image import ImageCaptcha

from flask import Blueprint, session, redirect, send_file

from base import logger as log, util, constant as const
from base.framework import general, TempResponse, url_for, form_check, db_conn, ErrorResponse, OkResponse
from base.logic import login_required
from base import dao
from base.poolmysql import transaction
from base.xform import F_str

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


@home.route("/register/load")
@general('注册页面')
def register_load():
    return TempResponse(const.DEVICE.PC + "/register.html")


@home.route("/register/load", methods=['POST'])
@general('注册')
@db_conn('db_writer')
@form_check({
    "username": F_str("用户名") & "strict" & "required",
    "password": F_str("密码") & "strict" & "required",
})
def register(db_writer, safe_vars):
    account = dao.get_account_by_username(db_writer, safe_vars.username)
    if account:
        return ErrorResponse("您，已经注册了!")
    with transaction(db_writer) as trans:
        # TODO:尚未考虑设备号
        is_ok, msg = dao.register(db_writer, safe_vars.username, safe_vars.password)
        if not is_ok:
            trans.finish()
            ErrorResponse(msg)
        trans.finish()

        session[const.SESSION.KEY_LOGIN] = is_ok
        session[const.SESSION.KEY_ADMIN_ID] = msg["user_id"]
        session[const.SESSION.KEY_ROLE_ID] = msg["role_id"]
        session.permanent = True

        log.get("auth").info("%s 注册成功 编号[%s]", safe_vars.username, msg["user_id"])
        return OkResponse(redirect=url_for("home.index"))


@home.route("/login")
@general("登录")
@db_conn("db_reader")
@form_check({
    "username": F_str("用户名") & "strict" & "required",
    "password": F_str("密码") & "strict" & "required",
})
def login(db_reader, safe_vars):
    account = dao.get_account_by_username(db_reader, safe_vars.username)
    if not account:
        return ErrorResponse("用户不存在")

    hash_pwd = util.hash_password(safe_vars.password, account.id)
    if hash_pwd != account.password:
        return ErrorResponse("密码错误")

    session[const.SESSION.KEY_LOGIN] = True
    session[const.SESSION.KEY_ADMIN_ID] = account.id
    session[const.SESSION.KEY_ROLE_ID] = account.role_id
    session.permanent = True
    log.get("auth").info("%s 登录成功 编号[%s]", safe_vars.username, account.id)
    return OkResponse()


@home.route("/captcha/image")
@general("获取图形验证码")
def get_image_captcha():
    captcha = ImageCaptcha()
    captcha_code = str(random.randint(1000, 9999))
    image = captcha.generate(captcha_code)
    session[const.SESSION.KEY_CAPTCHA] = captcha_code
    return send_file(image)


@home.route("/captcha/image/check")
@general("图片验证码验证")
@form_check({
    "image_captcha": F_str("图片验证码") & "strict" & "required",
})
def check_image_captcha(safe_vars):
    if safe_vars.image_captcha == session.get(const.SESSION.KEY_CAPTCHA):
        return OkResponse()
    return ErrorResponse("图片验证码错误，请重新输入")


@home.route("/logout")
@general("注销")
@login_required(const.ROLE.ALL)
def logout():
    session.clear()
    return redirect(url_for("home.login_load"))
