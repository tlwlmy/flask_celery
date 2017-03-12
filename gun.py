#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-03-12

import os
# import gevent.monkey
# gevent.monkey.patch_all()

# from meinheld import patch
# patch.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '0.0.0.0:8000'
pidfile = '/tmp/gunicorn.pid'
logfile = '/home/ymserver/log/flask_celery/gunicorn.log'

#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1 
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'
worker_class = 'meinheld.gmeinheld.MeinheldWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
