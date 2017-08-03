#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from app.datasource import redis_store
from app import db
from app.common.decorator import cached, del_cached
from app.common.constant import Duration
from app.common.base import model_insert, model_update
from .models import User

class AuthDb(object):
    """ 授权信息 """

    @cached(timeout=Duration.HalfHour)
    def query_user_lists(self, offset, limit):
        """ 查询用户列表 """

        record = User.query.offset(offset).limit(limit).all()

        return record

    @cached(timeout=Duration.HalfHour)
    def query_user_by_name(self, name):
        """ 根据用户姓名查询用户信息 """

        record = User.query.filter(User.name==name).first()

        return record

    @del_cached(keys=['modify_info'])
    def insert_user(self, modify_info):
        """ 插入用户信息 """

        record = model_insert(User, modify_info)

        # 格式化参数
        final = record._asdict()

        return final

    @del_cached(keys=['record', 'modify_info'], check=True)
    def update_user(self, record, modify_info):
        """ 更新用户信息 """

        # 更新跳转链接信息
        final = model_update(User, record, modify_info)

        return final


# 实例
auth_db = AuthDb()
