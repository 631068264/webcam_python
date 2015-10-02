#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ADM_ACCOUNT_STATUS(object):
    # 正常状态
    NORMAL = 0
    # 账号删除
    DELETED = 1


class ROLE(object):
    # 这里的ID和名字需要和数据库同步

    BOSS = 0
    BD_LEADER = 1
    BD_ASSISTANT = 2
    CAMPUS_AGENT = 3
    DEVELOPER = 4

    NAME_DICT = {
        BOSS: "总裁",
        BD_LEADER: "BD组长",
        BD_ASSISTANT: "BD助理",
        CAMPUS_AGENT: "校园代理",
        DEVELOPER: "开发人员",
    }

    ALL = NAME_DICT.keys()


class SESSION(object):
    # common
    KEY_LOGIN = "login"
    KEY_ADMIN_ID = "id"
    KEY_ADMIN_NAME = "name"
    KEY_ROLE_ID = "role_id"

    KEY_USER_ID = "user_id"

    # weixin
    KEY_OPEN_ID = "open_id"
    KEY_CAPTCHA = "image_captcha"


class COOKIES(object):
    KEY_LOGIN_OK_REDIRECT = "LOGINOKRE"
    KEY_REGISTER_OK_REDIRECT = "REGISTEROKRE"
    KEY_PASSWORD_OK_REDIRECT = "PASSWORDOKRE"
    KEY_VIEW_JOB_DETAIL_REDIRECT = "VIEWJOBREDIRECT"


class REDIS(object):
    ACCESS_TOKEN_KEY = "weixin:access_token"


class STATUS(object):
    SUCCESS = 1
    FAIL = 0
    NOT_LOGINED = 401


class ACCOUNT_STATUS(object):
    # 正常状态
    NORMAL = "NORMAL"
    # 锁住,往往因为密码被盗而锁住
    LOCKED = "LOCKED"
    # 下线状态
    OFFLINE = "OFFLINE"
    # 封禁状态
    BLOCKED = "BLOCKED"


class BALANCE_STATUS(object):
    NORMAL = "NORMAL"
    BLOCKED = "BLOCKED"


class CAPTCHA_USAGE(object):
    REGISTER = "REGISTER"
    RESET_PWD = "RESET_PWD"

    ALL = (REGISTER, RESET_PWD)


class WEIXIN_SUBSCRIBE_SOURCE(object):
    """
    微信关注来源:扫码
    """
    QRSCAN = "QRSCAN"
    """
    微信关注来源：其他
    """
    OTHER = "OTHER"


class PASSWORD_ACTION(object):
    RESET = "RESET"
    CHANGE = "CHANGE"

    ALL = (RESET, CHANGE)


class DEGREE(object):
    HIGH_SCHOOL = "高中"
    SECONDARY_SCHOOL = "中专"
    JUNIOR_COLLEGE = "大专"
    UNDER_GRADUATE = "本科"
    GRADUATE = "研究生"
    OTHER = "其他"

    ALL = (HIGH_SCHOOL, SECONDARY_SCHOOL, JUNIOR_COLLEGE, UNDER_GRADUATE, GRADUATE, OTHER)


class YES_NO(object):
    YES = "Y"
    NO = "N"

    ALL = (YES, NO)

    NAME_DICT = {
        YES: "是",
        NO: "否",
    }


class REGISTER_TYPE(object):
    EMPLOYER = "EMPLOYER"
    USER = "USER"
    ADMIN = "ADMIN"

    ALL = (EMPLOYER, USER, ADMIN)


class GENDER(object):
    FEMALE = "FEMALE"
    MALE = "MALE"

    ALL = (FEMALE, MALE)


class RECRUITMENT(object):
    class STATUS(object):
        # 未填写完整
        INCOMPLETE = "INCOMPLETE"

        # 正常状态
        NORMAL = "NORMAL"

        # 招聘取消
        CANCELED = "CANCELED"

        # 招聘已经结束:时间到了预设的时间
        ENDED = "ENDED"

        # 招聘已经完成:已经结算了，完成整个招聘流程
        FINISHED = "FINISHED"


class ADINFO_STATUS(object):
    NORMAL = "NORMAL"
    DELETE = "DELETE"


class OFFER_STATUS(object):
    # 等待录用
    WAITING = "WAITING"

    # 已录用
    EMPLOYED = "EMPLOYED"

    # 已取消（备招聘方取消）
    CANCELED = "CANCELED"

    # 已完成
    DONE = "DONE"

    NAME_DICT_USER = {
        WAITING: "报名中",
        EMPLOYED: "已录用",
        CANCELED: "被拒绝",
        DONE: "已完成",
    }


class SETTLE_PERIOD(object):
    # 日付
    DAILY = "DAILY"

    # 周付
    WEEKLY = "WEEKLY"

    # 月付
    MONTHLY = "MONTHLY"

    # 完结付
    FINISH = "FINISH"

    ALL = (DAILY, WEEKLY, MONTHLY, FINISH)

    NAME_DICT = {
        DAILY: "日结",
        WEEKLY: "周结",
        MONTHLY: "月结",
        FINISH: "完工结",
    }


class SALARY_UNIT(object):
    # 元/小时
    HOUR = "HOUR"

    # 元/天
    DAY = "DAY"

    # 元/周
    WEEK = "WEEK"

    # 元/月
    MONTH = "MONTH"

    ALL = (HOUR, DAY, WEEK, MONTH)

    NAME_DICT = {
        HOUR: "元/小时",
        DAY: "元/天",
        WEEK: "元/周",
        MONTH: "元/月",
    }


class ACCOUNT_RECOMMEND_INFO(object):
    class REFER_SOURCE(object):
        WEIXIN = "WEIXIN"
        ANDROID = "ANDROID"
        IOS = "IOS"
        FLYER = "FLYER"
        OTHER = "OTHER"
        BD = "BD"

    class REFERRER_ID_TYPE(object):
        ACCOUNT = "ACCOUNT"
        BD_ACCOUNT = "BD_ACCOUNT"


class COUPON(object):
    class STATUS(object):
        VALID = "VALID"
        INVALID = "INVALID"

    class TYPE(object):
        MONTHLY_FEE = "MONTHLY_FEE"
        YEARLY_FEE = "YEARLY_FEE"
        CASH = "CASH"

    ACTIVED = YES_NO


class SIGNATURE(object):
    KEY_SALT = "X-Digest"
    KEY_SIGNATURE = "X-Salt"


class OFFER_PAY_RESULT(object):
    # 未支付
    UN_PAYED = "UN_PAYED"

    # 已支付
    PAYED = "PAYED"

    # 支付失败
    PAY_FAILED = "PAY_FAILED"

    # 拒付
    WITHHOLD = "WITHHOLD"

    # 未设定
    UNSET = "UNSET"


class OFFER_RATE_RESULT(object):
    UN_RATE = "UN_RATE"
    FLOWER = "FLOWER"
    EGG = "EGG"


class COMMON_STATUS(object):
    NORMAL = "NORMAL"
    INVALID = "INVALID"
    BLOCKED = "BLOCKED"


class APP_TYPE(object):
    USER = 'USER'  # 学生端
    BUSINESS = 'BUSINESS'  # 商家端

    VALUES = {
        USER: 1,
        BUSINESS: 2,
    }

    ALL = (USER, BUSINESS)


class OS_TYPE(object):
    ANDROID = 'ANDROID'  # Android版
    IOS = 'IOS'  # iOS版

    VALUES = {
        ANDROID: 1,
        IOS: 2,
    }

    ALL = (ANDROID, IOS)


class DONE_JOB_STATUS(object):
    INIT = 0  # 初始状态
    CONFIRMED = 1  # 已确认


class EVENT(object):
    # 这里放各种事件类型，对应event_log中的event

    LOGIN = 1
    ENTER_HOME = 2

    NAMES = {
        LOGIN: '登录',
        ENTER_HOME: '打开首页'  # 具体可结合source
    }


class SOURCE(object):
    # 这里放各种来源, 对应event_log中的source和其他表中的来源字段

    UNDEFINED = 0
    WECHAT = 1
    ANDROID_USER = 2
    ANDROID_BUSINESS = 3
    BD = 4
    IOS_BUSINESS = 5

    NAMES = {
        UNDEFINED: '未知',
        WECHAT: '微信',
        ANDROID_USER: 'Android用户端',
        ANDROID_BUSINESS: 'Android商家端',
        BD: 'BD工具',
        IOS_BUSINESS: 'iOS商家端',
    }


class WECHAT_APP(object):
    OFFER_BASE_URL = "http://wx.msjz.la/weixin/jobs/view/?recruitment_id="
