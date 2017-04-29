#coding=utf-8

#=======客户端类型
CLIENT_TYPE_USER=0
CLIENT_TYPE_LOGINGATE=1
CLIENT_TYPE_LOGINSERVER=2

#=======ErrorCode
ERROR_OK=0
ERROR_MAX_LOGINGATE=1

#=======心跳包
KEEPLIVE=1


#=======登录网关服务器到登录网关管理服务器消息ID:[101-200]
LG2LGATEM_REQUEST_CONFIG=101

#=======登录网关管理服务器to登录网关服务器消息ID:[201-300]
LGATEM2LG_REPLY_CONFIG=201

#=======登录服务器到登录网关管理服务器消息ID:[301-400]
L2LGATEM_REQUEST_CONFIG=301

#=======登录网关管理服务器to登录服务器消息ID:[401-500]
LGATEM2L_REPLY_CONFIG=401