#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17


import json, random, string, hashlib, os
from decimal import Decimal
from flask import jsonify, make_response, request
from datetime import date, datetime
from functools import wraps, reduce
from app.common.constant import CM_STATIC_PATH

def api_response(contents, code=200):
    """返回API的响应
    :param contents: dict, JSON内容
    :param code: int, HTTP CODE
    :return: response
    """
    response = jsonify(contents)
    response.status_code = code
    return response

def replace_content(content, params):
    # 替换参数
    for key, value in params.items():
        content = content.replace('{' + key + '}', str(value))
    return content

def cover_none(key):
    # 转换None为字符串
    return '' if key is None else key

def random_lower_str(randomlength=5):
    # 随机长度字符串
    return ''.join(random.sample(string.ascii_lowercase, randomlength))

def random_int_str(randomlength=6):
    # 随机长度数字字符串
    return ''.join(map(str, [random.randint(0, 9) for i in range(0, randomlength)]))

def parse_url_params(url_conf, params):
    effect = True
    final = {}

    for key, conf in url_conf.items():
        if conf['need'] == 1:
            value = params.get(key, None)
            if value is None:
                effect = False
                continue
            final[key] = value
        else:
            final[key] = params.get(key, conf['default'])

        if final[key] is not None:
            if conf['type'] == 'i':
                final[key] = int(final[key])
            elif conf['type'] == 't':
                final[key] = datetime.fromtimestamp(int(final[key]))
            elif conf['type'] == 'd':
                final[key] = Decimal(final[key])

    return effect, final

def generate_str(final, dict_keys=[], symbol='&'):
    # 字典按照'&'分割转字符串

    if not dict_keys:
        dict_keys = final.keys()

    combine_str = symbol.join(["{0}={1}".format(key, final[key]) for key in dict_keys if key in final.keys()])
    return combine_str

def parse_str(combine_str):
    # 解析参数
    final = {}
    if combine_str.find('&') >= 0:
        for item in combine_str.split('&'):
            item = item.split('=')
            final[item[0]] = item[1]

    return final

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def md5(raw_str):
    # md5加密
    return hashlib.md5(raw_str.encode(encoding='utf-8')).hexdigest()

def parse_dict(final):
    # 拼接字典参数
    return '&'.join(['{0}={1}'.format(key, val) for key, val in final.items()])

def get_signature(params, secret):
    # 参数排序签名加secret拼接MD5签名
    keys = params.keys()
    keys.sort()

    sign_str = ''
    for key in keys:
        sign_str += "%s=%s&" % (key, params[key])

    #拼接上密钥
    sign_str += "%s=%s" % ("key", secret)
    return md5(sign_str).upper()

def url_dict_params(need, ktype, default='None', alias=None):
    """
    need: 参数是否必须 0表示不需要 1表示需要
    ktype: 参数类型 i表示整形 t表示时间戳 D表示Decimal
    default: 当need为不必要时默认值
    alias: 别名,使用参数名
    """

    final = {
        'need': need,
        'type': ktype,
    }

    # 默认值
    if default != 'None':
        final['default'] = default

    # 别名
    if alias is not None:
        final['alias'] = alias

    return final

def get_remote_ip():
    # 获取ip地址
    if 'X-Real-Ip' in request.headers.keys():
        return request.headers['X-Real-Ip']
    elif 'X-Forwarded-For' in request.headers.keys():
        return request.headers.getlist('X-Forwarded-For')[0]
    return request.remote_addr

def filter_fields(white_fields, modify_info):
    # 过滤参数

    final = {field: modify_info[field] for field in white_fields if field in modify_info.keys()}

    return final

def compare_fields(white_fields, record, modify_info):
    # 比较参数

    final = {field: modify_info[field] for field in white_fields if field in modify_info.keys() and modify_info[field] != record[field]}

    return final

def multi_lists_intersection(multi_lists):
    """
    多个列表交集
    @params list final: 多个列表集合
    @return list 返回交集列表
    """

    multi_lists = [set(lists) for lists in multi_lists]

    return list(reduce(lambda x,y:x&y, multi_lists))

def save_stream_img(filename, icon):
    """
    保存图片
    """

    # 文件位置
    target = os.path.join(CM_STATIC_PATH, filename)

    # 检查目录存不存在,如果不存在新建一个
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))

    with open(target,'wb') as up:
        up.write(icon)

    return target
