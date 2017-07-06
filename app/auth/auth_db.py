#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from app.datasource import redis_store
from app import db
from app.common.decorator import cached
from app.common.constant import Duration
from .models import User

class AuthDb(object):
    # 授权信息

    @cached(timeout=Duration.HalfHour)
    def query_user_by_name(self, name):
        # 根据用户姓名查询用户信息

        record = User.query.filter(User.name==name).first()

        return record

    def insert_user(self, modify_info):
        # 插入用户信息

        record = User.insert(modify_info=modify_info)

        # 更新uid查询缓存
        cache_key = "query_user_by_name:{0}".format(record.name)
        redis_store.delete(cache_key)

        # 格式化参数
        final = record._asdict()

        return final

    def update_user(self, record, modify_info):
        # 更新用户信息

        # 更新跳转链接信息
        affected_rows, final = User.update(record=record, modify_info=modify_info)

        # 无更新信息，直接返回
        if not final:
            return 0

        # 更新uid查询缓存
        cache_key = "query_user_by_name:{0}".format(record['name'])
        redis_store.delete(cache_key)

        return affected_rows

# 实例
auth_db = AuthDb()
