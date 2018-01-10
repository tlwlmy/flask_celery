#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-08-03

from .config_cache_auth import config_cache_auth

# 缓存映射配置
config_cache_map = {
    'app.auth': config_cache_auth,
}


def get_config_cache_map(module):
    """ 获取删除缓存方法 """

    # 文件路径
    path = module[:module.rindex('.')]

    # 文件名
    filename = module[module.rindex('.') + 1:]

    # 获取对应删除缓存keys方法
    func = config_cache_map[path][filename]

    return func
