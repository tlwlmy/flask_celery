#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-16

from app import create_app
from flask.ext.script import Manager
from flask import url_for

app = create_app()

manager = Manager(app)
if __name__ == '__main__':
    manager.run()
