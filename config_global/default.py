#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

IS_SEND_SMS = False
IS_VALIDATE_SIGNATURE = False
DEFAULT_CAPTCHA = "1234"
CAPTCHA_SEND_INTERVAL_SECONDS = 60
PAGE_SIZE = 20

URL_SIGN_KEY = "debug-key"
JWT_SECRET = "Hahaha, I am secret."

project_home = "hotgs"

debug = True
encoding = 'utf8'

debug_port = 5000

app_path = ''
static_path = '/static'
static_url_path = static_path


# MySQL配置
db_config = {
    "db_reader": {"host": "115.29.247.122", "port": 4206, "db": "djump",
                  "user": "djump", "passwd": "qwer1234", "charset": encoding},
    "db_writer": {"host": "115.29.247.122", "port": 4206, "db": "djump",
                  "user": "djump", "passwd": "qwer1234", "charset": encoding},
}

# Flask配置
app_config = {
    "permanent_session_lifetime": True,
    "SESSION_COOKIE_SECURE": True,
    "jwt_secret": JWT_SECRET,

    # cache type
    # "CACHE_TYPE": "filesystem",
    "CACHE_TYPE": "redis",

    "CACHE_DEFAULT_TIMEOUT": 86400,

    # cache for redis
    "CACHE_KEY_PREFIX": "dj_cache_",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_PASSWORD": "",
    "CACHE_REDIS_DB": 12,

    # # cache for filesystem
    # "CACHE_DIR": os.path.expanduser("cache/hotgs/"),
    # "CACHE_THRESHOLD": 500 * 1000,
}

pool_coroutine_mode = True
pool_log = "pool-log"

db_conn_pool_size = (3, 10)
db_connection_idle = 60
db_pool_clean_interval = 1000
db_query_log = "query-log"

redis_config = {}
redis_max_connections = 4
cache_TTL = 300

cache_memorized_job_list_timeout = 60 * 5
cache_memorized_timeout = 60 * 10
cache_index_page_timeout = 60 * 10
cache_page_timeout = 60 * 10

log_config = [
    ["pool-log", "pool.log", "debug"],
    ["query-log", "query.log", "debug"],

    ["response-log", "response.log", "debug"],
    ["cgi-log", "cgi.log", "debug"],
    ["root", "cgi.log", "debug"],
    ["auth", "auth.log", "debug"],
    ["tools-log", "tools.log", "debug"],
    ["interface-log", "interface.log", "debug"],
    ["sms-log", "sms.log", "debug"],
    ["wechat-log", "wechat.log", "debug"],
]


class FormCheckPattern(object):
    """
    前台表单控件的检查格式
    """

    # 手机号通用检查格式
    MOBILE_PATTERN = "^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$"

    # 手机号长度
    MOBILE_LEN = 11
