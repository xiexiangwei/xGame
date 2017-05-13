#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
import json
from common import fprotocol,const,CmdMessage_pb2
import clientmanager
import logging

def lg2sm_request_config(client, pkt):
    reply={u"error":const.ERROR_OK}
    active_id = clientmanager.instance.GetLogingateID()
    if active_id != None:
        loginserver_config = json.loads(pkt)
        clientmanager.instance.AddLogingate(active_id,loginserver_config[u"server_ip"],loginserver_config[u"server_port"])
        reply[u"id"]=active_id
        client.id = active_id
        client.type = const.CLIENT_TYPE_LOGINGATE
    else:
        reply[u"error"]=const.ERROR_MAX_LOGINGATE
    client.sendCmd(const.SM2LG_REPLY_CONFIG, json.dumps(reply))

def l2sm_request_config(client, pkt):
    reply = {u"error": const.ERROR_OK}
    active_id = clientmanager.instance.GetLoginServerID()
    if active_id != None:
        reply[u"id"] = active_id
        client.id = active_id
        client.type = const.CLIENT_TYPE_LOGINSERVER
    else:
        reply[u"error"] = const.ERROR_MAX_LOGINGATE
    client.sendCmd(const.SM2L_REPLY_CONFIG, json.dumps(reply))

#客户端请求管理服务器获取登录网关地址
def c2sm_get_logingate(client,pkt):
    '''
    reply={u"error":const.ERROR_OK}
    c_free_logingate = clientmanager.instance.GetFreeLoginGate()
    if c_free_logingate:
        reply[u"ip"]=c_free_logingate.ip
        reply[u"port"]=c_free_logingate.port
    else:
        reply[u"error"] =const.ERROR_NO_LOGINGATE
    client.sendCmd(const.SM2C_GET_LOGINGATE_REPLY, json.dumps(reply))
    '''
    reply = CmdMessage_pb2.RePly_Get_LoginGateInfo()
    reply.error=const.ERROR_OK
    c_free_logingate = clientmanager.instance.GetFreeLoginGate()
    if c_free_logingate:
        reply.ip = c_free_logingate.ip
        reply.port = c_free_logingate.port
    else:
        reply.error= const.ERROR_NO_LOGINGATE
    client.sendCmd(const.SM2C_GET_LOGINGATE_REPLY, reply.SerializeToString())


__cmdTable = {
                const.LG2SM_REQUEST_CONFIG:lg2sm_request_config,
                const.L2SM_REQUEST_CONFIG:l2sm_request_config,
                const.C2SM_GET_LOGINGATE:c2sm_get_logingate,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s",func.func_name)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
