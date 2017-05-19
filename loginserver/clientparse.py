#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
from common import fprotocol,const,CmdMessage_pb2
import json
import logging
import mysqlhelper


def Login(client,pkt):
    login_request = CmdMessage_pb2.Request_Login()
    login_request.ParseFromString(pkt)
    logging.debug(u"Login() account_name:%s account_pwd:%s",login_request.account_name,login_request.account_pwd)
    mysqlhelper.instance.Login(client,
                               login_request.account_name,
                               login_request.account_pwd)

__cmdTable = {
                const.C2LG_REQUEST_LOGIN:Login,
             }

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    func(clinet, pkt)

if __name__ == '__main__':
    pass
