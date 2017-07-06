#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from sqlalchemy.ext.declarative import declarative_base
from app import db
from functools import wraps
from app.common.functions import filter_fields, compare_fields

base = declarative_base()

class Base(db.Model):
    __abstract__ = True

    def validate(self):
        pass

    def save(self, validate=True, commit=False):
        if validate is True:
            self.validate()
        db.session.add(self)
        if commit is True:
            db.session.commit()

    def _asdict(self):
        # 获取参数字典

        final = self.__dict__
        if '_sa_instance_state' in final.keys():
            del final['_sa_instance_state']
        return final


def insert_filter(white_fields=[]):
    # 插入参数过滤装饰器
    def wrapper_fun(func):
        @wraps(func)
        def _wrapper_fun(*args, **kwargs):

            # 过滤参数
            kwargs['modify_info'] = filter_fields(white_fields, kwargs['modify_info'])

            # 调用插入方法
            record = func(*args, **kwargs)
            record.save(commit=True)

            return record
        return _wrapper_fun
    return wrapper_fun

def update_filter(white_fields=[]):
    # 更新参数过滤装饰器
    def wrapper_fun(func):
        @wraps(func)
        def _wrapper_fun(*args, **kwargs):

            # 过滤参数
            kwargs['modify_info'] = compare_fields(white_fields, kwargs['record'], kwargs['modify_info'])
            if kwargs['modify_info']:
                # 更新
                affected_row = func(*args, **kwargs)
                db.session.commit()

                return affected_row, kwargs['modify_info']

            return 0, {}

        return _wrapper_fun
    return wrapper_fun

