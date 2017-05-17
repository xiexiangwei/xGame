# coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import json
from common import fprotocol, const
import logging
import gamemanager


def ThreeCardServer2GC_Register(clinet, pkt):
    data = json.loads(pkt)
    clinet.SetCType(data[u"servertype"])
    clinet.SetSId(data[u"serverid"])
    gamemanager.instance.AddGame(data[u"servertype"],
                                 data[u"serverid"],
                                 data[u"serverip"],
                                 data[u"serverport"])



__cmdTable = {
    const.TCS2GC_REGISTER: ThreeCardServer2GC_Register
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
