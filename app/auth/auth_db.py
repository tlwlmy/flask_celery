#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from app.datasource import redis_store
from app import db
from app.common.decorator import cached, del_cached, del_multi_cached
from app.common.constant import Duration
from app.common.base import model_insert, model_update, model_insert_multi, model_update_multi
from .models import User

class AuthDb(object):
    """ 授权信息 """

    # @cached(rtype='dict', dict_keys=['uid'], timeout=Duration.HalfHour, qtype='multi_orm_query')
    @cached(rtype='dict', dict_keys=['uid'], timeout=0, qtype='multi_orm_query')
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

        final = model_update(User, record, modify_info)

        return final

    @del_multi_cached(keys=['modify_info'], rtype='list')
    def insert_multi_user(self, modify_info):
        """
        批量插入
        @params list modify_info: 用户列表信息
        @return list
        """

        record = model_insert_multi(User, modify_info)

        # 格式化参数
        final = [row._asdict() for row in record]

        return final

    @del_multi_cached(keys=['record', 'modify_info'])
    def update_multi_user(self, record,  modify_info):
        """
        批量插入
        @params dict record: 用户信息
        @params dict modify_info: 用户更新信息
        @return dict final: 最终更新信息
        """

        final = model_update_multi(User, record, modify_info)

        return final


# 实例
auth_db = AuthDb()
