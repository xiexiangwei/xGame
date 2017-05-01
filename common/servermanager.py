# coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
import logging
import fprotocol
import struct
import const
import json

START_TYPE_LOGINGATE=1
START_TYPE_LOGINSERVER=2



class ConfigException(Exception):
    "xGame Config Error"

class ServerManagerFactory(ReconnectingClientFactory):
    def __init__(self):
        ReconnectingClientFactory.maxDelay = 5

    def buildProtocol(self, addr):
        logging.info(u"servermanager is connected !")
        self.resetDelay()
        return instance

    def startedConnecting(self, connector):
        logging.info(u"servermanager is  connecting ...")

    def clientConnectionLost(self, connector, reason):
        logging.warn(u"servermanager connection is lost !")
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.warn(u"servermanager connect fail !")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class ServerManager(fprotocol.FProtocol):
    def __init__(self):
        fprotocol.FProtocol.__init__(self)
        self.startconfig = None
        self.callback = None
        self.isdaemon = False
        self.starttype = None

    def startLogingate(self, conf,callback,isdaemon):
        if conf.servermanager_ip == None:
            logging.error(u"没有配置登录网关管理服务器地址!")
            raise ConfigException
        if conf.servermanager_port == None:
            logging.error(u"没有配置登录网关管理服务器端口!")
            raise ConfigException
        reactor.connectTCP(conf.servermanager_ip,
                           conf.servermanager_port,
                           ServerManagerFactory())
        self.startconfig = conf
        self.callback = callback
        self.isdaemon = isdaemon
        self.starttype = START_TYPE_LOGINGATE

    def startLoginServer(self,conf,callback,isdaemon):
        if conf.servermanager_ip == None:
            logging.error(u"没有配置管理服务器地址!")
            raise ConfigException
        if conf.servermanager_port == None:
            logging.error(u"没有配置管理服务器端口!")
            raise ConfigException
        reactor.connectTCP(conf.servermanager_ip,
                           conf.servermanager_port,
                           ServerManagerFactory())
        self.startconfig = conf
        self.callback = callback
        self.isdaemon = isdaemon
        self.starttype = START_TYPE_LOGINSERVER

    def stop(self):
        pass

    def connectionMade(self):
        logging.info(u"servermanager.connectionMade()")
        fprotocol.FProtocol.reset(self)
        if self.starttype ==  START_TYPE_LOGINGATE:
            self.sendCmd(const.LG2SM_REQUEST_CONFIG,
                         json.dumps({'server_ip':self.startconfig.server_ip,
                                 'server_port':self.startconfig.server_port
                                 }
                                ))
        elif self.starttype == START_TYPE_LOGINSERVER:
            self.sendCmd(const.L2SM_REQUEST_CONFIG,
                         json.dumps({'server_ip': self.startconfig.server_ip,
                                     'server_port': self.startconfig.server_port
                                     }
                                    ))

    def packetReceived(self, cmd, pkt):
        if cmd in (const.SM2L_REPLY_CONFIG, const.SM2LG_REPLY_CONFIG):
            config = json.loads(pkt)
            if config[u"error"]==const.ERROR_OK:
                self.callback(self.isdaemon,config[u"id"])
                logging.debug(u"servermanager.packetReceived()")
        else:
            logging.warn(u"unknow cmd :%d",cmd)
instance = ServerManager()

if __name__ == '__main__':
    pass