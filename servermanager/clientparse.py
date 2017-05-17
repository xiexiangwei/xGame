# coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
import json
from common import fprotocol, const, CmdMessage_pb2
import clientmanager
import logging
import redishelper


def s2sm_request_start(client, pkt):
    reply = {u"error": const.ERROR_OK}
    server_config = json.loads(pkt)
    active_id = None
    if server_config[u"server_type"] == const.CLIENT_TYPE_LOGINGATE:
        active_id = clientmanager.instance.GetLogingateID()
    elif server_config[u"server_type"] == const.CLIENT_TYPE_LOGINSERVER:
        active_id = clientmanager.instance.GetLoginServerID()
    elif server_config[u"server_type"] == const.CLIENT_TYPE_GAMECENTER:
        active_id = 0
    elif server_config[u"server_type"] == const.CLIENT_TYPE_3CARD:
        active_id = clientmanager.instance.Get3CardID()

    if active_id != None:
        client.id = active_id
        client.type = server_config[u"server_type"]
        if server_config[u"server_type"] == const.CLIENT_TYPE_LOGINGATE:
            clientmanager.instance.AddLogingate(active_id, server_config[u"server_ip"], server_config[u"server_port"])
        elif server_config[u"server_type"] == const.CLIENT_TYPE_3CARD:
            clientmanager.instance.Add3Card(active_id, server_config[u"server_ip"], server_config[u"server_port"])
        reply[u"id"] = active_id
    else:
        reply[u"error"] = const.ERROR_SERVER_FULL
    client.sendCmd(const.SM2S_START_REPLY, json.dumps(reply))


# 客户端请求管理服务器获取登录网关地址
def c2sm_get_logingate(client, pkt):
    reply = CmdMessage_pb2.RePly_Get_LoginGateInfo()
    reply.error = const.ERROR_OK
    c_logingate = clientmanager.instance.DisLoginGate(client.getId())
    if c_logingate:
        reply.ip = c_logingate.ip
        reply.port = c_logingate.port
    else:
        reply.error = const.ERROR_NO_LOGINGATE
    client.sendCmd(const.SM2C_GET_LOGINGATE_REPLY, reply.SerializeToString())


# 客户端请求获取游戏中心地址
def c2sm_get_gamecenter(client, pkt):
    request = CmdMessage_pb2.Reply_Get_GameCenter()
    request.ParseFromString(pkt)
    logging.debug(u"c2sm_get_gamecenter() account_id:%s token:%s", request.account_id, request.token)
    # 验证token是否有效
    redishelper.instance.VerifyToken(client, request.account_id, request.token)


__cmdTable = {
    const.S2SM_REQUEST_START: s2sm_request_start,
    const.C2SM_GET_LOGINGATE: c2sm_get_logingate,
    const.C2SM_GET_GAMECENTER: c2sm_get_gamecenter,
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
