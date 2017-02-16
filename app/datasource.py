#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2016-09-22


from redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pymongo import MongoClient
import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

redis_store = StrictRedis(
    host=config.REDIS['host'],
    port=config.REDIS['port'],
    db=config.REDIS['db']
)

mongo = MongoClient(config.MONGO_URI, connect=False)
