#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016.07 tlwlmy
#

import logging
from logging.handlers import TimedRotatingFileHandler
from os import path
from app.common.config_log import LOGGING

class Loggers(object):
    """简单的logging wrapper"""

    def __init__(self):
        self.loggers = {}

    def get_logger(self, log_name, conf_name='default'):
        if log_name not in self.loggers.keys():
            logger = logging.getLogger(log_name)
            logger.setLevel(logging.INFO)
            if not logger.handlers:
                conf = LOGGING[conf_name]
                logger.setLevel(conf.get('level', logging.INFO))
                fh = TimedRotatingFileHandler(path.join(conf['path'], log_name), 'D', 1, conf.get('backups', 0))
                fh.setFormatter(logging.Formatter(conf.get('formatter', logging.BASIC_FORMAT)))
                logger.addHandler(fh)
            self.loggers[log_name] = logger
        return self.loggers[log_name]

loggers = Loggers()
