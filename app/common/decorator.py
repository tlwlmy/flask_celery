#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

import pickle
from app.datasource import redis_store
from app import db
from flask import request, make_response
from functools import wraps
from app.common.constant import Duration
from app.common.functions import multi_lists_intersection

def format_record(record, rtype, dict_keys):
    """
    格式化记录
    @params list|dict record: 数据
    @params str rtype: 返回类型 list表示列表 dict表示字典
    @params list dict_keys: 字典类型key列表
    @return list|dict
    """

    if isinstance(record, list) and rtype == 'dict':
        # 生产多重key数据
        final = {}

        # keys长度
        dict_keys_len = len(dict_keys)

        for row in record:
            # 利用字典可变性质，一层层生产字典
            r = final
            for index in range(0, dict_keys_len):
                key = row[dict_keys[index]]

                # 字典不存在则生成一个
                if key not in r.keys():
                    r[key] = {}

                # 到达最后一个key，直接指向当前行
                if index == dict_keys_len - 1:
                    r[key] = row
                r = r[key]

        return final

    return record

def single_orm_query(record):
    """ orm查询单行数据 """

    # 格式化
    final = record._asdict() if record else {}

    return final

def multi_orm_query(record):
    """ orm查询多行数据 """

    # 格式化
    final = [row._asdict() for row in record]

    return final

def single_raw_query(sql):
    """ 原生sql查询单行数据 """

    # 查询数据库
    record = db.session.execute(sql)

    # 获取第一条记录
    row = record.first() if record.rowcount else {}

    final = {key: value for key, value in row.items()}

    return final

def multi_raw_query(sql):
    """ 原生sql查询多行数据 """

    # 查询数据库
    record = db.session.execute(sql)

    final = [{key: value for key, value in row.items()} for row in record]

    return final

def format_query_record(record, qtype):
    """ 格式化查询参数 """

    if qtype == 'single_orm_query':
        # orm查询单行数据
        record = single_orm_query(record)
    elif qtype == 'multi_orm_query':
        # orm查询多行数据
        record = multi_orm_query(record)
    elif qtype == 'single_raw_query':
        # 原生sql查询单行数据
        record = single_raw_query(record)
    elif qtype == 'multi_raw_query':
        # 原生sql查询多行数据
        record = multi_raw_query(record)

    return record

def query_type(qtype='single_orm_query', rtype='list', dict_keys=[]):
    """ 查询缓存数据 """
    def wrapper_fun(func):
        @wraps(func)
        def _wrapper_fun(*args, **kwargs):
            """ _wrapper_fun"""

            # 根据查询类型查询
            record = format_query_record(func(*args, **kwargs), qtype)

            # 格式化查询参数
            final = format_record(record, rtype, dict_keys)

            return final
        return _wrapper_fun
    return wrapper_fun

def generate_cache_key(func_name, prefix, prefix_keys):
    """ 生产缓存key """
    cache_key = prefix if prefix is not None else func_name
    # cache_key = '{0}:{1}'.format(cache_key, ':'.join(map(str, prefix_keys)))
    for index in range(len(prefix_keys)):
        cache_key = '{0}:{1}'.format(cache_key, prefix_keys[index] if prefix_keys[index] is not None else '')
    return cache_key

def cached(prefix=None, rtype='list', dict_keys=[], timeout=Duration.HalfHour, func_type='class', qtype='single_orm_query'):
    """ 查询缓存数据 """
    def wrapper_fun(func):
        @wraps(func)
        def _wrapper_fun(*args, **kwargs):
            """ _wrapper_fun"""

            # 生产缓存key
            start_index = 1 if func_type == 'class' else 0
            cache_key = generate_cache_key(func.__name__, prefix, args[start_index:])

            # 外部修改缓存时长
            expire_time = kwargs['timeout'] if 'timeout' in kwargs.keys() else timeout

            # 删除timeout参数
            if 'timeout' in kwargs.keys():
                del kwargs['timeout']

            # 查询redis缓存数据
            final = redis_store.get(cache_key) if expire_time else None
            if final is None:
                # 查询数据库，格式数据库数据
                record = format_query_record(func(*args, **kwargs), qtype)

                # 格式化查询参数
                final = format_record(record, rtype, dict_keys)

                # 序列化参数，写缓存，设置缓存有效时间
                final = pickle.dumps(final)
                if expire_time:
                    redis_store.set(cache_key, final, expire_time)

            # 格式化参数
            final = pickle.loads(final)

            return final
        return _wrapper_fun
    return wrapper_fun

def del_cached(keys=['record', 'modify_info'], func_type='class', check=False):
    """ 删除缓存 """
    def wrapper_fun(func):
        @wraps(func)
        def _wrapper_fun(*args, **kwargs):
            """ _wrapper_fun"""

            # 查找参数初始坐标
            init_index = 1 if func_type == 'class' else 0

            # 格式参数
            final = {keys[index]: args[init_index + index] for index in range(0, len(keys))}

            # 检查字典是是否包含result键
            if 'result' in final.keys():
                raise Exception('result cannot in keys when delete cache')

            # 获取方法返回值
            result = func(*args, **kwargs)
            final['result'] = result

            # 如果需要检查，返回数据没有变化，不需要删除缓存
            if check == True and not final['result']:
                return result

            # 删除缓存
            from app.common.config_cache.functions import get_config_cache_map
            config_cache_map = get_config_cache_map(func.__module__)
            if func.__name__ in config_cache_map.keys():
                config_cache_map[func.__name__](final)

            return result

        return _wrapper_fun
    return wrapper_fun

def del_multi_cached(keys=['record', 'modify_info'], func_type='class', rtype='dict'):
    """ 批量删除缓存 """
    def wrapper_fun(func):
        @wraps(func)
        def _wrapper_fun(*args, **kwargs):
            """ _wrapper_fun"""

            # 查找参数初始坐标
            init_index = 1 if func_type == 'class' else 0

            # 格式参数
            final = {keys[index]: args[init_index + index] for index in range(0, len(keys))}

            # 检查字典是是否包含result键
            if 'result' in final.keys():
                raise Exception('result cannot in keys when delete cache')

            # 获取方法返回值
            result = func(*args, **kwargs)
            final['result'] = result

            # 删除缓存
            from app.common.config_cache.functions import get_config_cache_map
            config_cache_map = get_config_cache_map(func.__module__)

            # 检查数据类型
            if rtype == 'list':
                # 查询类别长度最小的key值
                min_len = min([len(final[key]) for key in keys])

                # 批量删除缓存
                for index in range(0, min_len):
                    data = {key: final[key][index] for key in keys}
                    data['result'] = final['result'][index]
                    config_cache_map[func.__name__](data)
            else:
                # 获取多个列表keys交集
                ekeys = multi_lists_intersection([final[key].keys() for key in keys])

                # 批量删除缓存
                for ekey in ekeys:
                    if final['result'][ekey]:
                        data = {key: final[key][ekey] for key in keys if final[key][ekey]}
                        data['result'] = final['result'][ekey]
                        config_cache_map[func.__name__](data)

            return result

        return _wrapper_fun
    return wrapper_fun

def del_cached_lists(func):
    """ 删除缓存 """
    def wrapper_fun(*args, **kwargs):
        """ wrapper_fun"""

        # 获取缓存key列表
        cache_keys = func(*args, **kwargs)

        # 删除缓存key
        for cache_key in cache_keys:
            redis_store.delete(cache_key)

        return cache_keys
    return wrapper_fun

def allow_cross_domain(func):
    """ 允许跨域 """
    @wraps(func)
    def wrapper_fun(*args, **kwargs):
        """ wrapper_fun"""

        rst = make_response(func(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

def allow_cookie_domain(func):
    """ 允许写cookie """
    @wraps(func)
    def wrapper_fun(*args, **kwargs):
        """ wrapper_fun"""

        rst = make_response(func(*args, **kwargs))
        http_origin = request.headers['Origin'] if 'Origin' in request.headers.keys() else '*'
        rst.headers['Content-type'] = 'application/json; charset=UTF-8'
        # rst.headers['Access-Control-Allow-Origin", "*")
        rst.headers['Access-Control-Allow-Origin'] = http_origin
        rst.headers['Access-Control-Allow-Credentials'] = 'true'
        rst.headers['Access-Control-Allow-Methods'] = '*'
        rst.headers['Access-Control-Allow-Headers'] = 'Content-Type,Accept,Authorization'
        rst.headers['Access-Control-Max-Age'] = '86400'
        return rst
    return wrapper_fun
