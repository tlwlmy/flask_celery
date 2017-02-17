#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim:fenc=utf-8
# @author tlwlmy
# @version 2017-02-17

# api 校验错误
PARAMETER_INCOMPLETE  = 401    # 参数不完整
PARAMETER_ILLEGAL     = 402    # 参数非法
PARAMETER_AUTH_FAILED = 403    # 签名校验失败
FORM_AUTH_FAILED      = 400    # 参数数据校验失败

# 服务器内部相关错误
INTERNAL_DB_ERROR = 500  # 数据库保存错误，或者其他相关数据库错误


# 基础错误码
EC_GET_PARAMS_MISSING      = -1001    # GET参数缺失
EC_POST_PARAMS_MISSING     = -1002    # POST参数缺失
EC_DELETE_PARAMS_MISSING   = -1003    # DELETE参数缺失
EC_PUT_PARAMS_MISSING      = -1004    # PUT参数缺失

EC_S_PARAMS_TOO_SHORT      = -1101    # s参数太短
EC_S_PARAMS_DECRYPT_ERROR  = -1102    # s参数解密失败
EC_CACHE_EXPIRE_TIME       = -1103    # 缓存超时
EC_MOBILE_FORMAT_ILLEGAL   = -1104    # 手机格式错误
EC_IP_NOT_IN_WHITE_LISTS   = -1105    # ip不在白名单中
EC_VALIDATE_KEY_ERROR      = -1106    # 验证码错误
EC_SINGLE_DEVICE_TOO_MUCH  = -1107    # 单个参数出现太多
EC_PAY_TYPE_FAILED         = -1108    # 效果类型错误
EC_PARAMS_MISSING          = -1109    # 参数错误
EC_RECORD_NOT_EXIST        = -1110    # 记录不存在
EC_RECORD_EXISTED          = -1111    # 记录已存在


# 用户错误码
EC_LOGIN_USER_NOT_EXIST        = -2001    # 用户不存在
EC_LOGIN_USER_EXPIRE           = -2002    # 用户登陆过期
EC_USER_ALIPAY_NOT_RIGHT       = -2003    # 用户支付宝账号错误
EC_USER_COST_OVERFLOW          = -2004    # 用户余额不足
EC_USER_VALIDATED_SIGNIN       = -2005    # 用户已验证用户关系
EC_USER_RELATIONSHIP_NOT_EXIST = -2006    # 用户关系不存在
EC_USER_NOT_VALIDATE_SIGNIN    = -2007    # 用户未验证关系
EC_LOGIN_USER_ACCOUNT_ERROR    = -2008    # 用户账号错误
EC_USER_DAY_SiGNINED           = -2009    # 用户已签到
EC_LOGIN_USER_UNAUTH           = -2010    # 用户登陆未授权
EC_USER_ACCOUNT_BAN            = -2011    # 用户被封杀
EC_USER_APP_WECHAT_BOUND       = -2012    # app用户已绑定微信
EC_USER_WECHAT_APP_BOUND       = -2013    # 微信已绑定app用户
EC_USER_APP_UNBIND_ERROR       = -2014    # app用户解绑微信公众号失败
EC_USER_HEADIMG_FORMAL_ERROR   = -2015    # 用户上传头像格式错误
EC_USER_NEWTASK_COMMIT_ILLEGAL = -2016    # 新手任务不允许提交
EC_USER_NEWTASK_COMPLETED      = -2017    # 新手任务已完成
EC_USER_VALID_MOBILE_TOO_MUCH  = -2018    # 用户验证手机次数太多
EC_USER_MOBILE_CODE_NOT_EXIST  = -2019    # 用户手机验证码不存在
EC_USER_MOBILE_CODE_ILLEGAL    = -2020    # 用户手机验证码不合法
EC_USER_BOUND_MOBILE           = -2021    # 用户已绑定手机
EC_MOBILE_BOUND_USER           = -2022    # 手机已绑定用户
EC_USER_BOUND_FATHER           = -2023    # 用户已绑定师傅
EC_USER_WX_PAY_UNBIND          = -2024    # 用户未绑定微信支付
EC_CHN_HELPER_NOT_FIND         = -2025    # 小助手渠道包找不到
EC_USER_INVITE_TOO_LITTLE      = -2026    # 用户邀请太少
EC_USER_VALIDATE_COUNT_ERROR   = -2027    # 用户验证次数错误
EC_USER_WECHAT_UNSUBSCRIBE     = -2028    # 用户未关注公众号
EC_USER_WX_PAY_FAIL            = -2029    # 用户支付失败
EC_USER_PAY_TASK_COMPLETED     = -2030    # 用户支付任务已完成
EC_USER_VALIDATE_FAIL          = -2031    # 用户验证失败
EC_REWARD_SHARE_DONE           = -2032    # 抽奖当天已分享
EC_REWARD_RAFFLE_ERROR         = -2033    # 抽奖次数不足
EC_COMMIT_TASK_UPLOAD_ERROR    = -2034    # 提审上传错误
EC_TASK_NOT_PRECDT             = -2035    # 任务无前提条件
EC_COMMIT_TASK_DISSATISFY      = -2036    # 提审条件不满足
EC_LIMIT_TASK_CLICKED          = -2037    # 任务已抢到


# 微信
EC_USER_WECHAT_AUTH_ERROR       = -2501    # 用户授权错误
EC_APP_WECHAT_CREATE_MENU_ERROR = -2502    # 创建菜单失败

# 广告
EC_AD_NOT_BUGDET                = -2701    # 广告没有预算
EC_AD_NOT_EFFECT                = -2702    # 广告无效



# 公众号错误码
EC_APPLICATION_NOT_FIND     = -3001    # 查不到公众号信息
EC_EXCHANGE_GIFT_NOT_EXIST  = -3002    # 兑换项不存在
EC_EXCHANGE_RECORD_NOT_EXIT = -3003    # 兑换记录不存在
EC_EX_RC_NOT_AUTH_MODIFY    = -3004    # 兑换记录没权限修改
EC_EX_RC_NOT_PERMIT_MODIFY  = -3005    # 兑换记录不可以修改
EC_EXCHANGE_GIFT_TOO_MUCH   = -3006    # 兑换太多
EC_EXCHANGE_GIFT_NOT_TARGET = -3007    # 没有定投兑换项
EC_SHARE_RATIO_NOT_EXIST    = -3008    # 分成项不存在

# 美赚
EC_CHN_CALLBACK_ORDER_EXIST = -4001    # 广告平台回调订单已存在
