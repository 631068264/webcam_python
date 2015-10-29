#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

IS_SEND_SMS = False
DEFAULT_CAPTCHA = "1234"
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

# 为保持清晰度延迟20秒
lazy = 10
# 添加同一任务的最多天数
add_same_task_max_day = 4

# MySQL配置
db_config = {
    "db_reader": {"host": "127.0.0.1", "port": 3306, "db": "webcap",
                  "user": "root", "passwd": "wuyuxi08", "charset": encoding},
    "db_writer": {"host": "127.0.0.1", "port": 3306, "db": "webcap",
                  "user": "root", "passwd": "wuyuxi08", "charset": encoding},
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
    ["auth", "auth.log", "debug"],
    ["interface-log", "interface.log", "debug"],
]


class FormCheckPattern(object):
    """
    前台表单控件的检查格式
    """

    # 手机号通用检查格式
    MOBILE_PATTERN = "^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$"

    # 手机号长度
    MOBILE_LEN = 11
