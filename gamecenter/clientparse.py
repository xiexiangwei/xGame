# coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import json
from common import fprotocol, const, CmdMessage_pb2
import logging
import gamemanager
import redishelper


def ThreeCardServer2GC_Register(clinet, pkt):
    data = json.loads(pkt)
    clinet.SetCType(data[u"servertype"])
    clinet.SetSId(data[u"serverid"])
    gamemanager.instance.AddGame(data[u"servertype"],
                                 data[u"serverid"],
                                 data[u"serverip"],
                                 data[u"serverport"])


def RequestEnterGameCenter(client, pkt):
    request = CmdMessage_pb2.Request_Enter_GameCenter()
    request.ParseFromString(pkt)
    logging.debug(u"RequestEnterGameCenter() account_id:%d token:%s", request.account_id, request.token)
    redishelper.instance.VerifyToken(client,
                                     request.account_id,
                                     request.token)


__cmdTable = {
    const.TCS2GC_REGISTER: ThreeCardServer2GC_Register,
    const.C2GC_REQUEST_ENTER_GC: RequestEnterGameCenter,
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
