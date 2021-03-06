#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''

import logging
import time
from twisted.internet import protocol
from common import fprotocol,const,CmdMessage_pb2
import clientfactory
import clientparse
import loginservermanager
import loginserver
import json
import redishelper

CLIENT_STATE_INIT               = 0
CLIENT_STATE_AUTH               = 1
CLIENT_STATE_LOGINED            = 2
CLIENT_STATE_TO_CLOSE           = 3


class Client(fprotocol.FProtocol):
    def __init__(self, pid, addr):
        fprotocol.FProtocol.__init__(self)
        self.__id = pid
        self.__addr = addr
        self.__ip = addr.host.decode('utf-8')
        self.toclosetime = time.time()
        self.state = CLIENT_STATE_INIT
        self.loginserver_id = None
        self.loginserver =  loginserver.LoginServer(self)

    def getId(self):
        return self.__id
    
    def getIp(self):
        return self.__ip

    def getState(self):
        return self.state
    
    def isLogined(self):
        return self.state==CLIENT_STATE_LOGINED
        
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
        #分配一个空闲的loginserver
        loginserverinfo = loginservermanager.instance.DisLoginServer(self.__id)
        if loginserverinfo:
            id = int(loginserverinfo[u"id"])
            ip = loginserverinfo[u"ip"]
            port = int(loginserverinfo[u"port"])
            logging.warn(u"分配用户空闲登录服务器成功 client_id:%d loginserver_id:%s loginserver_ip:%s loginserver_port:%s",self.getId(),id,ip,port)
            #分配成功之后，建立连接
            self.loginserver_id = id
            self.loginserver.start(ip,port)
        else:
            reply = CmdMessage_pb2.Reply_Connect_Logingate()
            reply.error = const.ERROR_NOT_READY_LOGIN
            self.sendCmd(const.LG2C_READY_LOGIN, reply.SerializeToString())

            self.kick()
            logging.warn(u"分配用户空闲登录服务器失败() client_id:%d",self.getId())
   
    def connectionLost(self, reason=protocol.connectionDone):
        logging.debug(u"Client.connectionLost %s", reason) 
        clientfactory.instance.removeProtocol(self)
        redishelper.instance.UpdateLoginServerTimes(self.loginserver_id, -1)
    
    def goToClose(self):
        self.state = CLIENT_STATE_TO_CLOSE
        self.toclosetime = time.time()
        
    def kick(self):
        logging.debug(u"Client.kick()")
        self.goToClose()

    def ReadyToLogin(self,ok):
        reply = CmdMessage_pb2.Reply_Connect_Logingate()
        reply.error = const.ERROR_OK
        if ok:
            redishelper.instance.UpdateLoginServerTimes(self.loginserver_id, 1)
        else:
            reply.error=const.ERROR_NOT_READY_LOGIN
        self.sendCmd(const.LG2C_READY_LOGIN, reply.SerializeToString())

    def Trans2Loginserver(self,cmd,pkt):
        if self.loginserver:
            self.loginserver.sendCmd(cmd,pkt)
        else:
            logging.error(u"玩家分配的登录服无效!")

