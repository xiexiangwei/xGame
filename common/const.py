#coding=utf-8

#=======客户端类型
CLIENT_TYPE_USER=0
CLIENT_TYPE_LOGINGATE=1
CLIENT_TYPE_LOGINSERVER=2

#=======ErrorCode
ERROR_OK=0
ERROR_MAX_LOGINGATE=1
ERROR_NO_LOGINGATE=2

#=======心跳包
KEEPLIVE=1


#=======登录网关服务器--->到管理服务器消息ID:[101-200]
LG2SM_REQUEST_CONFIG=101

#=======管理服务器--->登录网关服务器消息ID:[201-300]
SM2LG_REPLY_CONFIG=201

#=======登录服务器--->管理服务器消息ID:[301-400]
L2SM_REQUEST_CONFIG=301

#=======管理服务器--->登录服务器消息ID:[401-500]
SM2L_REPLY_CONFIG=401

#客戶端--->管理服务器消息ID:[501-600]
C2SM_GET_LOGINGATE=501

#管理服务器--->客戶端消息ID:[601-700]
SM2C_GET_LOGINGATE_REPLY=601

#客户端--->登录网关消息ID:[701-800]
C2LG_Login=701