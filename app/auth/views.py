#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

import time
from app.auth import auth
from flask import session, render_template
from app.auth.auth_db import auth_db
from app.common.functions import api_response, random_lower_str
from app.validate.functions import validate_params

@auth.route('/index', methods=['GET', 'POST'])
def index():
    return 'Hello world!'

@auth.route('/insert', methods=['POST'])
@validate_params
def insert(params):
    """ 插入用户 """

    # 查询用户名信息
    params['user_info'] = auth_db.query_user_by_name(params['input']['name'])
    if not params['user_info']:
        auth_db.insert_user(params['input'])
    else:
        auth_db.update_user(params['user_info'], params['input'])

    return api_response({'c': 0})

@auth.route('/insert_multi', methods=['GET'])
def insert_multi():
    """ 批量插入 """

    # 生成插入数据
    modify_info = []
    for index in range(0, 3):
        modify_info.append({
            'name': random_lower_str(10),
            'password': random_lower_str(10),
        })

    # 批量插入
    record = auth_db.insert_multi_user(modify_info)

    return api_response(record)

@auth.route('/update', methods=['POST'])
def update(params):

    record = auth_db.query_user_by_name(params['input']['name'])
    auth_db.update_user(record, params['input'])
    return api_response({'c'})

@auth.route('/update_multi', methods=['GET'])
def update_multi():
    """ 批量更新 """

    # 查询用户列表
    record = auth_db.query_user_lists(0, 2)

    modify_info = {}
    for ukey in record.keys():
        modify_info[ukey] = {
            'password': str(time.time())
        }

    # # 批量插入
    record = auth_db.update_multi_user(record, modify_info)

    return api_response(modify_info)

@auth.route('/admin')
def admin():
    """ 后台框架页面 """

    return render_template('index.html')

@auth.route('/lists', methods=['POST'])
@validate_params
def lists(params):
    """ 插入用户 """

    params['p'] = params['input']['p']
    params['l'] = params['input']['l']
    offset = (params['p'] - 1) * params['l']

    # 查询用户列表
    lists = auth_db.query_user_lists(offset, params['input']['l'])

    return api_response({'c': 0})
