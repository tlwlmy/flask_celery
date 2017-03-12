#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from app.auth import auth
from flask import session, render_template
from app.auth.auth_db import auth_db
from app.common.functions import api_response
from app.validate.functions import validate_params

@auth.route('/index', methods=['GET', 'POST'])
def index():
    return 'Hello world!'

@auth.route('/insert', methods=['POST'])
@validate_params
def insert(params):
    # 插入用户

    # 查询用户名信息
    params['user_info'] = auth_db.query_user_by_name(params['input']['name'])
    if not params['user_info']:
        auth_db.insert_user(params['input'])
    else:
        auth_db.update_user(params['user_info'], params['input'])

    return api_response({'c': 0})

@auth.route('/admin')
def admin():
    # 后台框架页面
    return render_template('index.html')
