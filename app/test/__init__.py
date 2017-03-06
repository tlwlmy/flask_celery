#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-25

from flask import Blueprint

test = Blueprint('test', __name__)

from . import views
