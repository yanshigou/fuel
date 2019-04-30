# -*- coding: utf-8 -*-


BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False

# 导入指定的任务模块
CELERY_IMPORTS = ('tools.tasks',)



