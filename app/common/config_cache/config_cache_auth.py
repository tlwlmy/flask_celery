#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-08-03

from app.common.decorator import del_cached_lists

@del_cached_lists
def insert_user(final): 
    """ 插入用户配置 """

    cache_keys = {
        'query_user_by_name:{0}'.format(final['modify_info']['name']),
        'query_user_by_uid:{0}'.format(final['result']['uid']),
    }
    
    return cache_keys

@del_cached_lists
def update_user(final): 
    """ 更新用户配置 """

    cache_keys = {
        'query_user_by_name:{0}'.format(final['record']['name']),
        'query_user_by_uid:{0}'.format(final['record']['uid']),
    }
    
    return cache_keys

config_cache_auth = {
    'auth_db': {
        'insert_user': insert_user,
        'insert_multi_user': insert_user,
        'update_user': update_user,
        'update_multi_user': update_user,
    },
}
