#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ACCOUNT_STATUS(object):
    # 正常状态
    NORMAL = 0
    # 账号删除
    DELETED = 1


class ROLE(object):
    # 这里的ID和名字需要和数据库同步

    ADMIN = 0
    NORMAL_ACCOUNT = 1

    NAME_DICT = {
        ADMIN: "管理员",
        NORMAL_ACCOUNT: "普通用户",
    }

    ALL = NAME_DICT.keys()


class STATUS(object):
    SUCCESS = 1
    FAIL = 0


class SESSION(object):
    # common
    KEY_LOGIN = "login"
    KEY_ADMIN_ID = "id"
    KEY_ROLE_ID = "role_id"
    KEY_CAPTCHA = "image_captcha"


class COOKIES(object):
    KEY_LOGIN_OK_REDIRECT = "LOGINOKRE"
    KEY_REGISTER_OK_REDIRECT = "REGISTEROKRE"
    KEY_PASSWORD_OK_REDIRECT = "PASSWORDOKRE"
    KEY_VIEW_JOB_DETAIL_REDIRECT = "VIEWJOBREDIRECT"


class CAPTCHA_USAGE(object):
    REGISTER = "REGISTER"
    RESET_PWD = "RESET_PWD"

    ALL = (REGISTER, RESET_PWD)


class PASSWORD_ACTION(object):
    RESET = "RESET"
    CHANGE = "CHANGE"

    ALL = (RESET, CHANGE)


class YES_NO(object):
    YES = "Y"
    NO = "N"

    NAME_DICT = {
        YES: "是",
        NO: "否",
    }

    ALL = NAME_DICT.keys()


class TASK_STATUS(object):
    # 正常状态
    NORMAL = 0
    # 账号删除
    DELETED = 1


class DEVICE(object):
    # 接入设备
    APP = "app"
    PC = "pc"
    ALL = (APP, PC)
