#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
from common import fprotocol,const
import json


def Login(client,pkt):
    data = json.loads(pkt)
    print data
    reply={u"error":const.ERROR_OK}
    client.sendCmd(const.L2LG_LOGIN_RESULT,json.dumps(reply))

__cmdTable = {
                const.C2LG_Login:Login,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
