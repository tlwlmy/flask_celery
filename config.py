#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2016-09-11

import redis

DEBUG = True

HOST = '0.0.0.0'

PORT = 5001

MONGO_URI = "mongodb://127.0.0.1:27017"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:tlwlmy@127.0.0.1:3306/dream?charset=utf8'

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

# session
SECRET_KEY = 'die32coajd$#!(dad)'
PERMANENT_SESSION_LIFETIME = 1800

SESSION_TYPE = 'redis'
SESSION_REDIS = redis.Redis(host='localhost',port=6379,db=0)

ROOT_PATH = '/home/ymserver/vhost/gateway/flask_celery'
LOG_PATH = "/home/ymserver/log/flask_celery/production-default.log" # 默认日志路径
