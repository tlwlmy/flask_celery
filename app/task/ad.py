#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-25


from flask import current_app, request
from celery.utils.log import get_task_logger
from app.auth.auth_db import auth_db
from functools import wraps
from app import create_app, celery


logger = get_task_logger(__name__)

@celery.task
def ad_platform_stat(message):
    app = create_app()
    with app.test_request_context():
        print(request.headers)

    print('message', message)
    logger.info(message)

    user_info = auth_db.query_user_by_name('tlwlmy')
    print(user_info)
