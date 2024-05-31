# -*- coding: utf-8 -*-
"""
@author:lpf
@file: celery_config.py
@time: 2023/8/7  17:17
"""
# 启用 UTC 时区
import os
from datetime import timedelta

# 时区,与django的TIMEZONE一致
CELERY_TIMEZONE = "Asia/Shanghai"

CELERY_TASK_TRACK_STARTED = True

# 有些情况防止死锁
CELERYD_FORCE_EXECV = True
# 任务失败允许重试
CELERY_ACKS_LATE = True
# Worker并发数量，一般默认CPU核数，可以不设置
CELERY_WORKER_CONCURRENCY = 2  # CELERYD_CONCURRENCY = 4
# 每个worker最多执行的任务数，超过这个就将worker进行销毁，防止内存泄漏，默认无限
CELERYD_MAX_TASKS_PER_CHILD = 8
CELERY_TASK_TIME_LIMIT = 36000
CELERY_RESULT_EXPIRES = 36000
# 任务限流
# CELERY_TASK_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

# 定时任务
