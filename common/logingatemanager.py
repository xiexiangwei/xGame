# coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
import logging
import fprotocol
import struct
import const
import json

class ConfigException(Exception):
    "xGame Config Error"

class LogingateManagerFactory(ReconnectingClientFactory):
    def __init__(self):
        ReconnectingClientFactory.maxDelay = 5

    def buildProtocol(self, addr):
        logging.info(u"logingatemanager is connected !")
        self.resetDelay()
        return instance

    def startedConnecting(self, connector):
        logging.info(u"logingatemanager is  connecting ...")

    def clientConnectionLost(self, connector, reason):
        logging.warn(u"logingatemanager connection is lost !")
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.warn(u"logingatemanager connect fail !")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class LogingateManager(fprotocol.FProtocol):
    def __init__(self):
        fprotocol.FProtocol.__init__(self)
        self.startconfig = None
        self.callback = None
        self.isdaemon = False

    def start(self, conf,callback,isdaemon):
        if conf.logingatemanager_ip == None:
            logging.error(u"没有配置登录网关管理服务器地址!")
            raise ConfigException
        if conf.logingatemanager_port == None:
            logging.error(u"没有配置登录网关管理服务器端口!")
            raise ConfigException
        reactor.connectTCP(conf.logingatemanager_ip,
                           conf.logingatemanager_port,
                           LogingateManagerFactory())
        self.startconfig = conf
        self.callback = callback
        self.isdaemon = isdaemon
    def stop(self):
        pass

    def connectionMade(self):
        logging.info(u"logingatemanager.connectionMade()")
        fprotocol.FProtocol.reset(self)
        self.sendCmd(const.L2LGATE_REQUEST_CONFIG,
                     json.dumps({'server_ip':self.startconfig.server_ip,
                                 'server_port':self.startconfig.server_port
                                 }
                                ))

    def packetReceived(self, cmd, pkt):
        config = json.loads(pkt)
        if config[u"error"]==const.ERROR_OK:
            self.callback(self.isdaemon)
            logging.debug(u"logingatemanager.packetReceived()")

instance = LogingateManager()

if __name__ == '__main__':
    pass