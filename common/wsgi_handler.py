#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
project_home = os.path.realpath(__file__)
project_home = os.path.split(project_home)[0]

import sys
sys.path.insert(0, os.path.split(project_home)[0])
sys.path.insert(0, project_home)

import redis
from flask import Flask

from etc import config
from base import constant as const
from base import smartpool, poolmysql
from base.util import text2html
from base.client_session import ItsdangerousSessionInterface
from base.framework import url_for, DjJsonResponse
from base import logger


# log setting
logger.init_log([(n, os.path.join("logs", p), l)
                 for n, p, l in config.log_config])


# pool setting
smartpool.coroutine_mode = config.pool_coroutine_mode
if config.debug and getattr(config, "pool_log", None) is not None:
    smartpool.pool_logger = logger.get(config.pool_log).info


# mysql setting
if config.debug and getattr(config, "db_query_log", None) is not None:
    poolmysql.query_logger = logger.get(config.db_query_log).info


for name, setting in config.db_config.iteritems():
    smartpool.init_pool(
        name, setting, poolmysql.MySQLdbConnection, *config.db_conn_pool_size,
        maxidle=config.db_connection_idle, clean_interval=config.db_pool_clean_interval
    )


app = Flask(__name__, static_url_path=config.app_path)
app.debug = config.debug
app.config.update(config.app_config)

# # cache
# cache.init_app(app)

# # redis session
# app.session_interface = RedisSessionInterface(redis.StrictRedis(
#     connection_pool=redis.ConnectionPool()))

app.session_interface = ItsdangerousSessionInterface()


# reg filters
from base import jinja_filter
for name, func in jinja_filter.mapping.iteritems():
    app.template_filter(name)(func)

app.jinja_env.globals['url_for'] = url_for


# reg exception handler
@app.errorhandler(500)
def handle_500(error):
    import traceback
    error_str = traceback.format_exc()
    logger.get("cgi-log").error(error_str)

    msg = error_str if config.debug else ""
    return DjJsonResponse(const.STATUS.FAIL, message=msg).output(), 200


@app.errorhandler(Exception)
def handle_exception(error):
    import traceback
    error_str = traceback.format_exc()
    logger.get("cgi-log").error(error_str)

    msg = error_str if config.debug else ""
    return DjJsonResponse(const.STATUS.FAIL, message=msg).output(), 200


@app.errorhandler(404)
def page_not_found(error):
    return DjJsonResponse(const.STATUS.FAIL, message='Not Found').output(), 404


# route setting
import views
for name in views.__all__:
    module = __import__('views.%s' % name, fromlist=[name])
    app.register_blueprint(getattr(module, name), url_prefix=config.app_path)


if __name__ == '__main__':
    os.environ['WSGI_CONFIG_MODULE'] = 'local'
    app.run(host='0.0.0.0',
            port=config.debug_port)
