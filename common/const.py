#coding=utf-8

#=======客户端类型
CLIENT_TYPE_USER=0
CLIENT_TYPE_LOGINGATE=1
CLIENT_TYPE_LOGINSERVER=2
CLIENT_TYPE_3CARD=3

#=======ErrorCode
ERROR_OK=0
ERROR_SERVER=1
ERROR_SERVER_FULL=2
ERROR_NO_LOGINGATE=4
ERROR_NOT_READY_LOGIN=5
ERROR_ACCOUNT_NOT_EXISTS=6
ERROR_ACCOUNT_PWD_ERROR=7

#=======心跳包
KEEPLIVE=1

#=======各种服务器--->到管理服务器消息ID:[101-200]
S2SM_REQUEST_START=101

#=======管理服务器--->各种服务器消息ID:[201-300]
SM2S_START_REPLY=201

#客戶端--->管理服务器消息ID:[501-600]
C2SM_GET_LOGINGATE=501

#管理服务器--->客戶端消息ID:[601-700]
SM2C_GET_LOGINGATE_REPLY=601

#客户端--->登录网关消息ID:[701-800]
C2LG_LOGIN=701

#登录网关--->客户端消息ID:[801-900]
LG2C_READY_TO_LOGIN=801
LG2C_LOGIN_RESULT=802

#登录服务器--->登录网关消息ID:[901-1000]
L2LG_LOGIN_RESULT=901
L2LG_TRANSFORM_CLIENT=902