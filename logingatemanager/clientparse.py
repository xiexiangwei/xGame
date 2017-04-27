#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
from common import fprotocol

def sendcmd(client,cmd,data):
    head = struct.pack("HH",len(data)+2,cmd)
    fmt = "%ds" % len(data)
    body = struct.pack(fmt,data)
    tail = struct.pack("H",0)
    senddata = head+body+tail
    client.sendCmd(senddata)

def test(client,pkt):
    pass

__cmdTable = {
                888:test,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
