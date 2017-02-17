#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

import re, urllib
from datetime import datetime
from decimal import Decimal
from functools import wraps
from flask import request, session, redirect, url_for, make_response
from app.common.config_error import EC_LOGIN_USER_UNAUTH, EC_GET_PARAMS_MISSING
from app.common.functions import api_response, get_remote_ip
from .auth_config_params import auth_url_params

def parse_url_params(url_conf, params):
    # 解析参数
    effect, final = True, {}

    for key, conf in url_conf.items():
        # 是否修改参数名
        alias = conf['alias'] if 'alias' in conf.keys() else key

        # 获取参数值
        if key in params.keys():
            final[alias] = params[key]
        else:
            if conf['need'] == 1:
                effect = False
                continue
            if 'default' in conf.keys():
                final[alias] = conf['default']

        if alias in final.keys() and final[alias] is not None:
            # 检查参数类型
            if conf['type'] == 'i':
                if isinstance(final[alias], int) or final[alias].isdigit():
                    final[alias] = int(final[alias])
                else:
                    effect = False
            elif conf['type'] == 't':
                if isinstance(final[alias], int) or final[alias].isdigit():
                    final[alias] = datetime.fromtimestamp(int(final[alias]))
                else:
                    effect = False
            elif conf['type'] == 'D':
                if re.match('^\d+(\.\d+)?$', final[alias]):
                    final[alias] = Decimal(final[alias])
                else:
                    effect = False

    return effect, final

def get_params_config(module, func_name, method):
    # 获取url解析配置
    # 获取url解析配置
    if module.find('app.auth.') >= 0:
        if func_name in auth_url_params.keys():
            return auth_url_params[func_name][method]
    return{}

def get_request_data():
    # 获取请求参数
    if request.method == 'GET':
        return request.args
    elif request.method == 'POST':
        return request.form
    return {}

def get_params(module, func_name, method):
    # 获取url参数
    config_params = get_params_config(module, func_name, method)

    # 获取请求参数
    data = get_request_data()

    return parse_url_params(config_params, data)

def format_init_params(func):
    # 格式化初始参数
    @wraps(func)
    def wrapper_fun(*args, **kwargs):
        params = kwargs['params'] if 'params' in kwargs.keys() else {}

        # 获取请求基本信息
        params['ip'] = get_remote_ip()
        params['ipr'] = request.remote_addr
        params['ua'] = urllib.parse.quote(request.headers['User-Agent'], safe='')

        kwargs['params'] = params

        return func(*args, **kwargs)
    return wrapper_fun

def validate_admin_user(func):
    # 验证用户信息
    @wraps(func)
    def wrapper_fun(*args, **kwargs):
        # 验证用户信息

        name = session.get('name', None)
        if name is None:
            return redirect(url_for('auth.login'))

        # 解析url参数
        effect, params = get_params(func.__module__, func.__name__, request.method)
        if effect == False:
            return api_response({'c': EC_GET_PARAMS_MISSING, 'msg': 'params_error'})

        # 格式参数
        if params:
            if 'params' not in kwargs.keys():
                kwargs['params'] = {}
            kwargs['params']['input'] = params

        return func(*args, **kwargs)
    return wrapper_fun

def validate_params(func):
    # 验证参数
    @wraps(func)
    @format_init_params
    def wrapper_fun(*args, **kwargs):
        # 解析url参数
        effect, params = get_params(func.__module__, func.__name__, request.method)
        if effect == False:
            return api_response({'c': EC_GET_PARAMS_MISSING, 'msg': 'params_error'})

        # 格式参数
        if 'params' not in kwargs.keys():
            kwargs['params'] = {}
        kwargs['params']['input'] = params

        return func(*args, **kwargs)
    return wrapper_fun
