# coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
import logging
from common import fprotocol,const
import struct
import json

class ConfigException(Exception):
    "xGame Config Error"

class ServerManagerFactory(ReconnectingClientFactory):
    def __init__(self):
        ReconnectingClientFactory.maxDelay = 5

    def buildProtocol(self, addr):
        logging.info(u"servermanager is connected !")
        self.resetDelay()

    def startedConnecting(self, connector):
        logging.info(u"servermanager is  connecting ...")

    def clientConnectionLost(self, connector, reason):
        logging.warn(u"servermanager connection is lost !")
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.warn(u"servermanager connect fail !")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class ServerManager(fprotocol.FProtocol):
    def __init__(self,robot):
        fprotocol.FProtocol.__init__(self)
        self.startconfig = None
        self.robot = robot

    def start(self, conf):
        if conf.servermanager_ip == None:
            logging.error(u"没有配置登录网关管理服务器地址!")
            raise ConfigException
        if conf.servermanager_port == None:
            logging.error(u"没有配置登录网关管理服务器端口!")
            raise ConfigException
        reactor.connectTCP(conf.servermanager_ip,
                           conf.servermanager_port,
                           ServerManagerFactory())

    def stop(self):
        pass

    def connectionMade(self):
        logging.info(u"servermanager.connectionMade()")
        self.robot.GetLoginGate()


    def packetReceived(self, cmd, pkt):
        logging.info(u"servermanager.packetReceived()")
        if cmd==const.SM2C_GET_LOGINGATE_REPLY:
            self.robot.OnGetLoginGate(pkt)


if __name__ == '__main__':
    pass