#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-16

from flask import Flask
from app.datasource import redis_store
from flask_session import Session
from celery import Celery
from config import CELERY_BROKER_URL
from flask_sqlalchemy import SQLAlchemy

celery = Celery(__name__, broker=CELERY_BROKER_URL)
sess = Session()
db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object('config')
    sess.init_app(app)
    db.init_app(app)

    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOG_PATH'],
                                       maxBytes=1024*1024, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    celery = make_celery(app)

    # 授权
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 任务
    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/task')

    # 测试
    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint, url_prefix='/test')

    return app

def make_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
