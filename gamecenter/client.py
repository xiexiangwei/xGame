# coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''

import logging
import time

from twisted.internet import protocol

import clientparse
from common import fprotocol, const
import gamemanager

CLIENT_STATE_INIT = 0
CLIENT_STATE_AUTH = 1
CLIENT_STATE_LOGINED = 2
CLIENT_STATE_TO_CLOSE = 3


class Client(fprotocol.FProtocol):
    def __init__(self, pid, addr):
        fprotocol.FProtocol.__init__(self)
        self.__id = pid
        self.__addr = addr
        self.__ip = addr.host.decode('utf-8')
        self.toclosetime = time.time()
        self.state = CLIENT_STATE_INIT
        # 客户端类型
        self.__ctype = const.CLIENT_TYPE_USER
        # 服务器ID
        self.__sid = None

    def getId(self):
        return self.__id

    def getIp(self):
        return self.__ip

    def getState(self):
        return self.state

    def SetCType(self, t):
        self.__ctype = t

    def GetCType(self):
        return self.__ctype

    def SetSId(self, sid):
        self.__sid = sid

    def GetSId(self):
        return self.__sid

    def isLogined(self):
        return self.state == CLIENT_STATE_LOGINED

    def packetReceived(self, cmd, pkt):
        if self.state == CLIENT_STATE_TO_CLOSE:
            return
        try:
            clientparse.parse(self, cmd, pkt)
        except Exception:
            logging.exception(u"clientparse.parse() cmd=%d" % cmd)
            self.abort()

    def connectionMade(self):
        logging.debug(u"Client.connectionMade() ip=%s", self.__ip)

    def connectionLost(self, reason=protocol.connectionDone):
        logging.debug(u"Client.connectionLost %s", reason)
        if self.__ctype != const.CLIENT_TYPE_USER and self.__sid is not None:
            gamemanager.instance.RemoveGame(self.__ctype, self.__sid)

    def goToClose(self):
        self.state = CLIENT_STATE_TO_CLOSE
        self.toclosetime = time.time()

    def kick(self):
        logging.debug(u"Client.kick()")
        self.goToClose()
