# coding=utf-8

from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
import logging
from common import fprotocol,const
import json

class ConfigException(Exception):
    "xGame Config Error"

class LogingateFactory(ClientFactory):
    def __init__(self, logingate):
        self.logingate = logingate

    def buildProtocol(self, addr):
        logging.warn(u" Logingate CONNECTED!!!")
        return self.logingate

    def startedConnecting(self, connector):
        ClientFactory.startedConnecting(self, connector)
        logging.warn(u" Logingate connecting!!!")

    def clientConnectionLost(self, connector, reason):
        ClientFactory.clientConnectionLost(self, connector, reason)
        logging.warn(u" Logingate DOWN!!!")
        self.logingate.onConnectionLost()

    def clientConnectionFailed(self, connector, reason):
        ClientFactory.clientConnectionFailed(self, connector, reason)
        logging.warn(u" Logingate connect FAIL!!!")
        self.logingate.connectionFail()


class Logingate(fprotocol.FProtocol):
    def __init__(self,robot):
        fprotocol.FProtocol.__init__(self)
        self.factory =  LogingateFactory(self)
        self.robot = robot

    def start(self, ip,port):
        reactor.connectTCP(ip, port,self.factory)

    def stop(self):
        pass

    def connectionMade(self):
        logging.info(u"servermanager.connectionMade()")


    def connectionFail(self):
        pass

    def onConnectionLost(self):
        pass

    def packetReceived(self, cmd, pkt):
        logging.info(u"servermanager.packetReceived() cmd:%d pkt:%s",cmd,pkt)
        if cmd == const.LG2C_READY_TO_LOGIN:
            reply = json.loads(pkt)
            if reply[u"error"]==const.ERROR_OK:
                self.robot.Login()
        elif cmd == const.LG2C_LOGIN_RESULT:
            reply = json.loads(pkt)
            if reply[u"error"]==const.ERROR_OK:
                logging.debug(u"机器人登录成功! robot:%d",self.robot.id)
                self.abort()
                logging.debug(u"机器人断开网关!准备进入游戏! robot:%d",self.robot.id)



if __name__ == '__main__':
    pass