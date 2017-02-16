#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-16

from flask import Flask
from app.datasource import db, redis_store
from flask.ext.session import Session

sess = Session()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object('config')
    sess.init_app(app)

    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOG_PATH'],
                                       maxBytes=1024*1024, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.remove()

    return app
