"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/18-12:53
INSTRUCTIONS:   celery 初始配置
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'activate-tas': {
#         'task': 'api.equipments.tasks.activate',
#         'schedule': crontab(minute='*/10')
#     }
# }
