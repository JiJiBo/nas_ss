# -*- coding: utf-8 -*-
"""
@author:lpf
@file: celery.py
@time: 2023/7/27  17:22
"""
import os

from celery import Celery

from nas_ss import settings

# 设置django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nas_ss.settings') # 项目配置

# 创建celery实例化对象
app = Celery('nas_ss')   # 项目名

# 启动项目celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现项目中的tasks
app.autodiscover_tasks(settings.INSTALLED_APPS)
