#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import urlparse

from etc import config as cfg
from base.smartsql import Table as T, Field as F, Expr as E, QuerySet as QS
from base import constant as const
from base.cache import cache
from base.framework import url_for
from base import util


def get_account_by_user_id(db, user_id):
    user = QS(db).table(T.account).where(F.id == user_id).select_one("*")
    return user


def get_account_by_username(db, username):
    user = QS(db).table(T.account).where(F.username == username).select_one("*")
    return user


def get_company_by_owner(db, user_id):
    company = QS(db).table(T.company).where(F.owner == user_id).select_one("*")
    # 因为之前的接口，数据库字段是下划线命名，而返回的Json中又变成了驼峰命名法，因为不想在数据库使用AS，
    # 所以在返回的地方转一下。F**K
    return util.convert_dict_key_underscore2camelcase(company)


def get_user_profile(db, user_id):
    user_profile = QS(db).table(T.user_profile).where(F.id == user_id).select_one("*")
    return util.convert_dict_key_underscore2camelcase(user_profile)


def get_user_data_profile(db, user_id):
    user_data_profile = QS(db).table(T.user_data_profile).where(F.id == user_id).select_one("*")
    return util.convert_dict_key_underscore2camelcase(user_data_profile)


def get_user_education(db, user_id):
    education = QS(db).table(T.education).where(F.id == user_id).select_one("*")
    return util.convert_dict_key_underscore2camelcase(education)


def get_user_balance(db, user_id):
    education = QS(db).table(T.balance).where(F.id == user_id).select_one("*")
    return util.convert_dict_key_underscore2camelcase(education)
