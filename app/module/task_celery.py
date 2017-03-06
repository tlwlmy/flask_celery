#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016.05.04 tlwlmy
#

from config import CELERY_BROKER_URL
from celery import Celery

class TaskCelery():
    __celery = None

    def __init__(self):
        # 初始化Celery
        self.__celery = Celery(broker=CELERY_BROKER_URL)

    def __del__(self):
        # 关掉Celery链接
        self.__celery.close()

    def send_user_inform(self, message, queue='user_inform') :
        # 发送广告统计数据
        self.__celery.send_task('app.task.user.user_inform', (message,), queue=queue, compression='zlib', serializer='json')


# 实例
task_celery = TaskCelery()
