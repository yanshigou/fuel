# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/4/30"
import os
from celery import Celery, platforms

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuel.settings')

app = Celery("fuel_celery")
platforms.C_FORCE_ROOT = True
app.config_from_object('tools.celeryconf')  # 加载配置模块