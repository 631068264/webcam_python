#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from flask import session
from flask import request, redirect

from base import constant as const
from base.framework import Redirect, DjErrorResponse
from base.framework import url_for
from base.util import decode_from_access_token


def login_required():
    """
    检查用户的登录/注册状态，默认依次检查：登录/注册，开关
    """

    def new_deco(old_handler):
        @wraps(old_handler)
        def new_handler(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            session = decode_from_access_token(access_token)

            # TODO fix
            if session:
                return old_handler(*args, **kwargs)
            else:
                return DjErrorResponse(u"未登录", status=const.STATUS.NOT_LOGINED)

        return new_handler

    return new_deco


def admin_required(roles=None):
    def new_deco(old_handler):
        """
        检查管理员的登录状态
        """

        @wraps(old_handler)
        def new_handler(*args, **kwargs):
            logined = session.get(const.SESSION.KEY_LOGIN)
            if logined:
                role_id = session.get(const.SESSION.KEY_ROLE_ID)
                if roles is None or (isinstance(roles, str) and role_id == roles) or role_id in roles:
                    return old_handler(*args, **kwargs)
            else:
                return Redirect(url_for("home.login_load"))

        return new_handler

    return new_deco


def bd_required(roles=None):
    def new_deco(old_handler):
        """
        检查管理员的登录状态
        """

        @wraps(old_handler)
        def new_handler(*args, **kwargs):
            logined = session.get(const.SESSION.KEY_LOGIN)
            if logined:
                role_id = session.get(const.SESSION.KEY_ROLE_ID)
                if roles is None or (isinstance(roles, str) and role_id == roles) or role_id in roles:
                    return old_handler(*args, **kwargs)
            else:
                return redirect(url_for("bd.login_load"))

        return new_handler

    return new_deco


def wechat_required(ret_json=False):
    def new_deco(old_handler):
        """
        检查微信公众号用户的登录状态
        """

        @wraps(old_handler)
        def new_handler(*args, **kwargs):
            logined = session.get(const.SESSION.KEY_LOGIN)
            if logined:
                return old_handler(*args, **kwargs)
            else:
                return Redirect(url_for("user.login_load"))

        return new_handler

    return new_deco


def wechat_required_not_login():
    def new_deco(old_handler):
        """
        需要用户未登录
        """

        @wraps(old_handler)
        def new_handler(*args, **kwargs):
            logined = session.get(const.SESSION.KEY_LOGIN)
            if logined:
                return Redirect(url_for("jobs.job_list"))
            else:
                return old_handler(*args, **kwargs)

        return new_handler

    return new_deco
