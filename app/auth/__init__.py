#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17


from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
