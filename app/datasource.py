#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2016-09-22


import boto3
from redis import StrictRedis
from pymongo import MongoClient
import config

redis_store = StrictRedis(
    host=config.REDIS['host'],
    port=config.REDIS['port'],
    db=config.REDIS['db']
)

mongo = MongoClient(config.MONGO_URI, connect=False)

s3 = boto3.resource(
    's3',
    region_name=config.AWS['region'],
    aws_access_key_id=config.AWS['access_key_id'],
    aws_secret_access_key=config.AWS['secret_access_key']
)
