#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-03-06

from app.test import test
from app.common.functions import api_response
from app.module.task_celery import task_celery

@test.route('/user_inform', methods=['GET'])
def user_inform():
    # 测试通知用户信息

    message = {
        'uid': 1,
        'inform': u'Hello Word!',
    }

    from app.task.user import user_inform
    message = user_inform(message)
    # message = task_celery.send_user_inform(message)

    return api_response(message)
