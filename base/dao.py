#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base import util


def get_account_by_username(db, username):
    return QS(db).table(T.account).where(
        (F.username == username) & (F.status == const.ACCOUNT_STATUS.NORMAL)
    ).select_one()


def register(db, username, password):
    user_id = util.gen_user_id(username)
    hash_pwd = util.hash_password(password, user_id)

    QS(db).table(T.account).insert({
        "id": user_id,
        "username": username,
        "password": hash_pwd,
        "name": None,
        "device": None,
        "status": const.ACCOUNT_STATUS.NORMAL,
        "role_id": const.ROLE.NORMAL_ACCOUNT,
    })
    msg = {
        "user_id": user_id,
        "role_id": const.ROLE.NORMAL_ACCOUNT,
        "username": username,
    }
    return True, msg
