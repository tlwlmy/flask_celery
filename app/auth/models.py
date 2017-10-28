#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from datetime import datetime
from app import db
from app.common.base import Base

class User(Base):
    """ 用户 """
    __tablename__ = 'user'
    uid = db.Column('uid', db.Integer, primary_key=True)    # 用户id
    name = db.Column('name', db.String(64))    # 用户名
    password = db.Column('password', db.String(32), default='')    # 用户密码
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)    # 创建时间
    last_edit = db.Column('last_edit', db.DateTime, default=datetime.now)    # 最后编辑时间

    # 插入数据库列表
    _insert_fields = ['name', 'password']

    # 更新数据库字段列表
    _update_fields = ['password']
