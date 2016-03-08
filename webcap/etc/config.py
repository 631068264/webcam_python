#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config_global import *

# app context path
app_path = "/webcam"

debug_port = 80
static_path = '/static'
static_url_path = static_path

# 为保持清晰度延迟20秒
lazy = 5
# 添加同一任务的最多天数
add_same_task_max_day = 4
# 任务开始前2小时不能删除
min_hours_left_when_cancel = 2

client_port = 10218
data_buffer = 1024 * 10
