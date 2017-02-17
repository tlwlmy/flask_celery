#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

from app.common.functions import url_dict_params

auth_url_params = {
    'login': {
        'GET': {},
        'POST': {
            'username': url_dict_params(1, 's', None, 'name'),
            'password': url_dict_params(1, 's'),
        }
    },
    'insert': {
        'POST': {
            'username': url_dict_params(1, 's', None, 'name'),
            'password': url_dict_params(1, 's'),
        }
    },
    'update': {
        'POST': {
            'username': url_dict_params(1, 's', None, 'name'),
            'password': url_dict_params(1, 's'),
        }
    },
}
