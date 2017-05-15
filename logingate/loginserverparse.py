#coding=utf-8
import struct
from common import fprotocol,const
import logging
import json

def keeplive(clinet,pkt):
    pass

def l2lg_transform_client(client,pkt):
    data = json.loads(pkt)
    logging.debug(u"l2lg_transform_client parse() data:%s",data)
    client.send2client(data[u"cmd"], data[u"pkt"].encode('unicode-escape').decode('string_escape'))

def l2lg_login_result(client,pkt):
    logging.debug(u"l2lg_login_result() pkt:%s",pkt)
    if client.user:
        client.user.sendCmd(const.LG2C_LOGIN_RESULT,pkt)
    else:
        logging.error(u"l2lg_login_result() 玩家句柄无效")


__cmdTable = {
                const.KEEPLIVE:keeplive,
                const.L2LG_TRANSFORM_CLIENT: l2lg_transform_client,
                const.L2LG_LOGIN_RESULT: l2lg_login_result,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"loginserver parse() func:%s",func.func_name)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
