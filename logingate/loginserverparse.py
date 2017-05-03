#coding=utf-8
import struct
from common import fprotocol,const
import logging

def keeplive(clinet,pkt):
    pass

def l2lg_login_result(client,pkt):
    logging.debug(u"l2lg_login_result() pkt:%s",pkt)
    if client.user:
        client.user.sendCmd(const.LG2C_LOGIN_RESULT,pkt)
    else:
        logging.error(u"l2lg_login_result() 玩家句柄无效")


__cmdTable = {
               const.KEEPLIVE:keeplive,
               const.L2LG_LOGIN_RESULT: l2lg_login_result,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
