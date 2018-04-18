#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from app import db
from sqlalchemy import exc
from functools import wraps
from app.common.functions import filter_fields, compare_fields

class Base(db.Model):
    __abstract__ = True

    def validate(self):
        pass

    def save(self, validate=True, commit=False):
        """ 保存 """

        if validate is True:
            self.validate()
        db.session.add(self)
        if commit is True:
            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()

    def _asdict(self):
        """ 获取参数字典 """

        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

def get_primary_key(obj):
    """ 获取主键名 """
    return obj.__mapper__.primary_key[0].name

def model_insert(obj, modify_info):
    """ 插入 """

    # 过滤参数
    modify_info = filter_fields(obj._insert_fields, modify_info)

    # 插入参数
    record = obj(**modify_info)
    record.save(commit=True)

    return record

def model_update(obj, record, modify_info):
    """ 更新 """

    modify_info = compare_fields(obj._update_fields, record, modify_info)

    if not modify_info:
        return {}

    # 获取主键
    primary_key = get_primary_key(obj)

    # 更新数据
    affected_row = obj.query.filter(getattr(obj, primary_key)==record[primary_key]).update(modify_info)
    db.session.commit()

    return modify_info

def model_insert_multi(obj, modify_info):
    """
    批量插入
    @params record dict: 返回类型 list表示列表 dict表示字典
    @params modify_info dict: 字典类型key列表
    """

    # 过滤列表参数
    for index in range(0, len(modify_info)):
        modify_info[index] = filter_fields(obj._insert_fields, modify_info[index])

    # 批量插入
    record = [obj(**modify_info[index]) for index in range(0, len(modify_info))]
    db.session.add_all(record)
    db.session.commit()

    return record

def model_update_multi(obj, record, modify_info):
    """
    批量更新
    @params record dict: 返回类型 list表示列表 dict表示字典
    @params modify_info dict: 字典类型key列表
    """

    # 过滤列表参数
    for ukey in modify_info.keys():
        if ukey in record.keys():
            modify_info[ukey] = compare_fields(obj._update_fields, record[ukey], modify_info[ukey])

    # 获取主键
    primary_key = get_primary_key(obj)

    # 更新列表数据
    for ukey in modify_info.keys():
        if modify_info[ukey] and ukey in record.keys():
            affected_row = obj.query.filter(getattr(obj, primary_key)==record[ukey][primary_key]).update(modify_info[ukey])

    db.session.commit()

    return modify_info
