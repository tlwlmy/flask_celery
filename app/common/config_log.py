#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2016-09-11

LOGGING = {
    "default": {
        "path": "/data/log/default",
        "formatter": "[%(asctime)s: %(levelname)s] %(message)s",
        "level": 20,  # 20:info; 40:error
        "backups": 30,  # backup count
    },
    "celery": {
        "path": "/data/log/celery",
        "formatter": "[%(asctime)s: %(levelname)s] %(message)s",
        "level": 20,  # 20:info; 40:error
        "backups": 30,  # backup count
    },
}
