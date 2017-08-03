#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2016-09-22


from redis import StrictRedis
from pymongo import MongoClient
import config

redis_store = StrictRedis(
    host=config.REDIS['host'],
    port=config.REDIS['port'],
    db=config.REDIS['db']
)

mongo = MongoClient(config.MONGO_URI, connect=False)
