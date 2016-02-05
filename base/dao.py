#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

from base.smartsql import Table as T, Field as F, QuerySet as QS
from base import constant as const
from base import util


def register(db, username, password):
    hash_pwd = util.hash_password(password, username)
    user_id = util.get_id()
    QS(db).table(T.account).insert({
        "id": user_id,
        "username": username,
        "password": hash_pwd,
        "name": None,
        "status": const.ACCOUNT_STATUS.NORMAL,
        "role_id": const.ROLE.NORMAL_ACCOUNT,
    })

    msg = {
        "user_id": user_id,
        "role_id": const.ROLE.NORMAL_ACCOUNT,
        "username": username,
    }
    return True, msg


def get_account_by_username(db, username):
    return QS(db).table(T.account).where(
        (F.username == username) & (F.status == const.ACCOUNT_STATUS.NORMAL)
    ).select_one()


def get_account_by_id(db, account_id):
    return QS(db).table(T.account).where(
        (F.id == account_id) & (F.status == const.ACCOUNT_STATUS.NORMAL)
    ).select_one()


def get_devices_by_account_id(db, account_id):
    return QS(db).table(T.device).where(
        (F.account_id == account_id) & (F.status == const.DEVICE_STATUS.NORMAL)
    ).select()


def update_device_by_account_id(db, account_id, device_id):
    return QS(db).table(T.device).where(
        (F.account_id == account_id) & (F.id == device_id) & (F.status == const.DEVICE_STATUS.NORMAL)
    ).select_one(for_update=True)


def update_task_by_account_id(db, account_id, task_id):
    return QS(db).table(T.task).where(
        (F.account_id == account_id) & (F.status != const.TASK_STATUS.DELETED) & (F.id == task_id)
    ).select_one(for_update=True)


def update_src_by_account_id(db, account_id, src_id):
    return QS(db).table(T.src).where(
        (F.account_id == account_id) & (F.status == const.TASK_STATUS.NORMAL) & (F.id == src_id)
    ).select_one(for_update=True)


def get_device_by_account_id(db, account_id, device_id):
    return QS(db).table(T.device).where(
        (F.account_id == account_id) & (F.id == device_id) & (F.status == const.DEVICE_STATUS.NORMAL)
    ).select_one()


def get_tasks_by_account_id(db, account_id):
    return QS(db).table(T.task).where(
        (F.account_id == account_id) & (F.status != const.TASK_STATUS.DELETED)
    ).order_by(F.create_time, desc=True).select()


def get_task_device(db, task_id):
    return QS(db).table((T.task__t * T.device__d).on(F.t__device_id == F.d__id)).where(
        (F.t__id == task_id) & (F.d__status == const.DEVICE_STATUS.NORMAL) & (F.t__status == const.TASK_STATUS.NORMAL)
    ).select_one("t.*", for_update=True)


def get_srcs_by_account_id(db, account_id):
    return QS(db).table(T.src).where(
        (F.account_id == account_id) & (F.status == const.SRC_STATUS.NORMAL)
    ).order_by(F.create_time, desc=True).select()


def get_tasks_by_account_and_device(db, account_id, device_id):
    return QS(db).table(T.task).where(
        (F.account_id == account_id) & (F.device_id == device_id) & (F.status != const.TASK_STATUS.DELETED)
    ).select()


def get_device_by_accountId_and_name(db, account_id, device_name):
    return QS(db).table(T.device).where(
        (F.account_id == account_id) & (F.name == device_name)
    ).select_one()
