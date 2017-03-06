#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-03-06


import json
from app.module.loggers import loggers
from app.module.task_celery import task_celery
from app import create_app, celery
from app.common.functions import CJsonEncoder


@celery.task
def user_inform(message):
    # 发送用户信息

    logger = loggers.get_logger('user_inform.log', 'celery')

    app = create_app()
    with app.test_request_context():
        logger.info(json.dumps(message, cls=CJsonEncoder))
