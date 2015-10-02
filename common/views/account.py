#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import random
import urlparse
import datetime
from flask import Blueprint, request, session

from base import constant as const
from base.constant import STATUS
from base import dblogic as dbl
from base import util
from base.framework import json_check, form_check, general, db_conn
from base.poolmysql import transaction
from base.framework import DjJsonResponse, login_required
from base.smartsql import Table as T, Field as F, Expr as E, QuerySet as QS
from base.xform import F_str, F_mobile, F_int
from base import logger
from etc import config as cfg


account = Blueprint("account", __name__)


@account.route("/api/v1/captcha", methods=["GET"])
@general("获取短信验证码接口")
@db_conn("db_writer")
@form_check({
    "mobile": F_mobile(u"手机号码") & "strict" & "required",
    "usage": F_str(u"验证码用途") & "strict" & "required" & (
        lambda v: (v in const.CAPTCHA_USAGE.ALL, v)),
})
def get_captcha(db_writer, safe_vars):
    account = dbl.get_account_by_username(db_writer, safe_vars.mobile)
    if safe_vars.usage == const.CAPTCHA_USAGE.RESET_PWD:
        if not account:
            return DjJsonResponse(STATUS.FAIL, message=u"账号不存在")
    elif safe_vars.usage == const.CAPTCHA_USAGE.REGISTER:
        if account:
            return DjJsonResponse(STATUS.FAIL, message=u"账号已经注册存在")

    # TODO 增加次数限制

    captcha = random.randint(100000, 999999)

    captcha_msg = u"您的验证码是：%s。" % captcha
    if not util.send_sms(safe_vars.mobile, captcha_msg):
        return DjJsonResponse(STATUS.FAIL, message=u"发送验证码失败")

    QS(db_writer).table(T.captcha).insert({
        "mobile": safe_vars.mobile,
        "captcha": captcha,
        "send_time": datetime.datetime.now(),
        "usage": safe_vars.usage,
        "used": const.YES_NO.NO,
        "ip": util.safe_inet_aton(request.remote_addr),
    })

    token = util.gen_sms_token(safe_vars.usage, safe_vars.mobile, captcha)
    return DjJsonResponse(STATUS.SUCCESS, token=token)


@account.route("/api/v1/register", methods=["POST"])
@general("注册接口")
@db_conn("db_writer")
@json_check({
    "username": F_mobile(u"用户名") & "strict" & "required",
    "password": F_str(u"密码") & "strict" & "required",
    "token": F_str(u"token") & "strict" & "required",
    "captcha": F_str(u"验证码") & "strict" & "required",
    "type": F_str(u"类型") & "strict" & "required" & (lambda v: (v in const.REGISTER_TYPE.ALL, v)),
})
def register(db_writer, safe_vars):
    account = dbl.get_account_by_username(db_writer, safe_vars.username)
    if account:
        return DjJsonResponse(STATUS.FAIL, message=u"用户已经注册过了")

    # 检查token是否正确
    token = util.gen_sms_token(const.CAPTCHA_USAGE.REGISTER, safe_vars.username, safe_vars.captcha)
    if token != safe_vars.token:
        logger.debug(token)
        logger.debug(safe_vars.token)
        return DjJsonResponse(STATUS.FAIL, message=u"验证码不正确.")

    with transaction(db_writer) as trans:
        # 检测是否有未使用的验证码
        captcha_row = QS(db_writer).table(T.captcha) \
            .where((F.mobile == safe_vars.username) & (F.used == const.YES_NO.NO)) \
            .order_by(F.id, desc=True).select_one("*", for_update=True)
        if not captcha_row:
            return DjJsonResponse(STATUS.FAIL, message=u"不存在未使用短信")

        if captcha_row.captcha != safe_vars.captcha:
            logger.debug(captcha_row.captcha)
            logger.debug(safe_vars.captcha)
            return DjJsonResponse(STATUS.FAIL, message=u"验证码不正确")

        # 标记验证码为使用
        QS(db_writer).table(T.captcha).where(F.id == captcha_row.id).update({"used": const.YES_NO.YES})

        # 创建一个用户
        # TODO 这里user_id可能会冲突
        user_id = util.gen_user_id(safe_vars.username)
        hash_pwd = util.hash_password(safe_vars.password, user_id)

        QS(db_writer).table(T.account).insert({
            "id": user_id,
            "username": safe_vars.username,
            "password": hash_pwd,
            "create_time": datetime.datetime.now(),
            "type": safe_vars.type,       # TODO 这里需要校验请求是从哪里发出来的
            "status": const.ACCOUNT_STATUS.NORMAL,
        })

        QS(db_writer).table(T.user_profile).insert({
            "id": user_id,
            "gender": const.GENDER.FEMALE,
            "phone": safe_vars.username,
            "age": 0,
        })

        QS(db_writer).table(T.user_data_profile).insert({
            "id": user_id,
        })

        company_id = QS(db_writer).table(T.company).insert({
            "owner": user_id,
        })

        QS(db_writer).table(T.company_data_profile).insert({
            "id": company_id,
        })

        QS(db_writer).table(T.user_location).insert({
            "id": user_id,
            "province": "",
            "city": "",
            "district": "",
            "street": "",
            "longitude": 0,
            "latitude": 0,
            "update_time": datetime.datetime.now(),
        })

        QS(db_writer).table(T.balance).insert({
            "id": user_id,
            "cash": 0,
            "monthly_fee": 0,
            "yearly_fee": 0,
            "update_time": datetime.datetime.now(),
            "status": const.BALANCE_STATUS,
        })

        trans.finish()

        return DjJsonResponse(STATUS.SUCCESS, token=token)


@account.route("/api/v1/login", methods=["POST"])
@general("登录接口")
@db_conn("db_reader")
@json_check({
    "username": F_str(u"用户名") & "strict" & "required",
    "password": F_str(u"密码") & "strict" & "required",
})
def login(db_reader, safe_vars):
    account = dbl.get_account_by_username(db_reader, safe_vars.username)
    if not account:
        return DjJsonResponse(STATUS.FAIL, message=u"用户不存在")

    hash_pwd = util.hash_password(safe_vars.password, account.id)

    account = QS(db_reader).table(T.account).where(
        (F.username == safe_vars.username) & (F.password == hash_pwd)).select_one("*")
    if not account:
        return DjJsonResponse(STATUS.FAIL, message=u"用户密码不正确")

    params = {
        "id": account.id,
        "nick": account.nick,
        "avatar": account.avatar,
        "company": dbl.get_company_by_owner(db_reader, account.id),
        "profile": dbl.get_user_profile(db_reader, account.id),
        "accessToken": util.gen_access_token(account.id),
    }
    return DjJsonResponse(STATUS.SUCCESS, **params)


@account.route("/api/v1/profile", methods=["GET"])
@login_required()
@general("获取个人信息")
@db_conn("db_reader")
def get_profile(db_reader):
    user_id = session["user_id"]

    user = dbl.get_account_by_user_id(db_reader, user_id)
    company = dbl.get_company_by_owner(db_reader, user_id)
    education = dbl.get_user_education(db_reader, user_id)
    balance = dbl.get_user_balance(db_reader, user_id)

    profile = dbl.get_user_profile(db_reader, user_id)
    profile.education = education
    profile.balance = balance
    profile.company = company
    profile.nick = user.nick
    profile.dataProfile = dbl.get_user_data_profile(db_reader, user_id)
    # 头像如果为空，返回名字第一个字符
    profile.avatar = user.avatar if user.avatar else (profile.name[0] if profile.name else "")

    params = {
        "profile": profile,
    }
    return DjJsonResponse(STATUS.SUCCESS, **params)


@account.route("/api/v1/profile", methods=["POST"])
@login_required()
@general("修改个人信息")
@db_conn("db_writer")
@json_check({
    "name": F_str(u"名字") & "strict" & "required",
    "gender": F_str(u"性别") & "strict" & "required",
    "age": (1 <= F_int(u"年龄", default_value=0) <= 200) & "optional",
    "degree": F_str(u"学历") & "optional" & (lambda v: (v in const.DEGREE.ALL, v)),
    "intro": F_str(u"简介") & "optional",
})
def update_profile(db_writer, safe_vars):
    user_id = session["user_id"]

    with transaction(db_writer) as trans:
        data = {
            "id": user_id,
            "name": safe_vars.name,
            "gender": safe_vars.gender,
            "age": safe_vars.age,
            "intro": safe_vars.intro,
        }
        QS(db_writer).table(T.user_profile).insert(data, on_duplicate_key_update=data)

        QS(db_writer).table(T.education).insert({
            "id": user_id,
            "degree": safe_vars.degree,
        }, on_duplicate_key_update={"degree": E("VALUES(degree)")})

        trans.finish()

    return DjJsonResponse(STATUS.SUCCESS)
