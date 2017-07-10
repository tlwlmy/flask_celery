#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app import db
from app.common.base import Base, insert_filter, update_filter

class User(Base):
    # 用户
    __tablename__ = 'user'
    uid = db.Column('uid', Integer, primary_key=True)    # 用户id
    name = db.Column('name', String(64))    # 用户名
    password = db.Column('password', String(32), default='')    # 用户密码
    create_time = db.Column('create_time', DateTime, default=datetime.now)    # 创建时间
    last_edit = db.Column('last_edit', DateTime, default=datetime.now)    # 最后编辑时间

    # 插入数据库列表
    _insert_fields = ['name', 'password']

    # 更新数据库字段列表
    _update_fields = ['password']

    @staticmethod
    @insert_filter(_insert_fields)
    def insert(modify_info):
        # 插入
        record = User(**modify_info)

        return record

    @staticmethod
    @update_filter(_update_fields)
    def update(record, modify_info):
        # 更新
        affected_row = User.query.filter(User.uid==record['uid']).update(modify_info)

        return affected_row, modify_info

