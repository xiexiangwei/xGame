#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
import json
from common import fprotocol,const
import clientmanager

def l2lgate_request_config(client,pkt):
    reply={u"error":const.ERROR_OK}
    client.type = const.CLIENT_TYPE_LOGINGATE
    active_id = clientmanager.instance.GetLogingateID()
    if active_id != None:
        loginserver_config = json.loads(pkt)
        clientmanager.instance.AddLogingate(active_id,loginserver_config[u"server_ip"],loginserver_config[u"server_port"])
        reply[u"id"]=active_id
    else:
        reply[u"error"]=const.ERROR_MAX_LOGINGATE
    client.sendCmd(const.LGATE2L_REPLY_CONFIG,json.dumps(reply))

__cmdTable = {
                const.L2LGATE_REQUEST_CONFIG:l2lgate_request_config,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
