#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

import os

CM_ROOT_PATH = os.getcwd()    # 根目录
CM_SATIC_PATH = os.path.join(CM_ROOT_PATH, 'app/static')    # 静态文件目录

# 用户
USER_DEFAULT_HEAD_IMG_URL = 'http://{0}/static/headimg/headimg.png'    # 微信用户默认头像

# AES加密密钥
AES_ENCRYPT_SECRET = 'df23b1699fba9ec7bd4b7bbc57d46e6b'

# 公众号类型
APP_WECHAT_TYPE_AUTH_SERVER      = 0    # 认证服务号
APP_WECHAT_TYPE_UNAUTH_SERVER    = 1    # 未认证服务号
APP_WECHAT_TYPE_UNAUTH_SUBSCRIBE = 2    # 未认证订阅号


PRICE_EXCHANGE_RATE = 1000    # 积分兑换比例 1元等于1000积分

# 手机平台
MOBILE_PLATFORM_IOS     = 1
MOBILE_PLATFORM_ANDROID = 2

# 后台登录账号
BACKGROUND_LOGIN_USER_NAME = 'xiaopao'    # 后台登录用户名
BACKGROUND_LOGIN_PASSWORD  = 'jitui123'   # 后台登录用户密码

# 微信用户授权跳转链接
USER_WECHAT_AUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}#wechat_redirect'

# 缓存的有效时间
class Duration:
    HalfMin   = 30;
    OneMin    = 60;
    TwoMin    = 120;
    ThrMin    = 180;
    FiveMin   = 300;
    TenMin    = 600;
    FifMin    = 900;
    TwentyMin = 1200;
    HalfHour  = 1800;
    OneHour   = 3600;
    TwoHour   = 7200;
    FiveHour  = 18000;
    HalfDay   = 43200;
    OneDay    = 86400;
    TenDay    = 864000;
