#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import struct
from common import fprotocol,const,CmdMessage_pb2
import json
import logging


def Login(client,pkt):
    login_request = CmdMessage_pb2.Request_Login()
    login_request.ParseFromString(pkt)
    logging.debug(u"Login() account_name:%s account_pwd:%s",login_request.account_name,login_request.account_pwd)

    reply = CmdMessage_pb2.Reply_Login()
    reply.error = const.ERROR_OK
    if login_request.account_name and login_request.account_pwd:
        logging.debug(u"登录成功")
    client.send2client(const.LG2C_LOGIN_RESULT,reply.SerializeToString())

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
