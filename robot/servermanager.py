# coding=utf-8

from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
import logging
from common import fprotocol,const
import struct
import json

class ConfigException(Exception):
    "xGame Config Error"

class ServerManagerFactory(ClientFactory):
    def __init__(self, sm):
        self.sm = sm

    def buildProtocol(self, addr):
        logging.warn(u"ServerManager CONNECTED!!!")
        return self.sm

    def startedConnecting(self, connector):
        ClientFactory.startedConnecting(self, connector)
        logging.warn(u"ServerManager connecting!!!")

    def clientConnectionLost(self, connector, reason):
        ClientFactory.clientConnectionLost(self, connector, reason)
        logging.warn(u"ServerManager DOWN!!!")
        self.sm.onConnectionLost()

    def clientConnectionFailed(self, connector, reason):
        ClientFactory.clientConnectionFailed(self, connector, reason)
        logging.warn(u"ServerManager connect FAIL!!!")
        self.sm.connectionFail()


class ServerManager(fprotocol.FProtocol):
    def __init__(self,robot):
        fprotocol.FProtocol.__init__(self)
        self.factory =  ServerManagerFactory(self)
        self.robot = robot

    def start(self, conf):
        if conf.servermanager_ip == None:
            logging.error(u"没有配置管理服务器地址!")
            raise ConfigException
        if conf.servermanager_port == None:
            logging.error(u"没有配置管理服务器端口!")
            raise ConfigException
        reactor.connectTCP(conf.servermanager_ip,
                           conf.servermanager_port,
                           self.factory)
    def stop(self):
        pass

    def connectionMade(self):
        logging.info(u"servermanager.connectionMade()")
        self.robot.GetLoginGate()

    def connectionFail(self):
        pass

    def onConnectionLost(self):
        pass

    def packetReceived(self, cmd, pkt):
        logging.info(u"servermanager.packetReceived()")
        if cmd==const.SM2C_GET_LOGINGATE_REPLY:
            self.robot.OnGetLoginGate(pkt)




if __name__ == '__main__':
    pass