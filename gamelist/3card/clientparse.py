#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
from common import fprotocol,const
import logging

__cmdTable = {

             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
