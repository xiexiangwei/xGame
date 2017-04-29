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
        self.starttype = None

    def startLogingate(self, conf,callback,isdaemon):
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
        self.starttype = START_TYPE_LOGINGATE

    def startLoginServer(self,conf,callback,isdaemon):
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
        self.starttype = START_TYPE_LOGINSERVER

    def stop(self):
        #TODO：断开socket连接
        pass

    def connectionMade(self):
        logging.info(u"logingatemanager.connectionMade()")
        fprotocol.FProtocol.reset(self)
        if self.starttype ==  START_TYPE_LOGINGATE:
            self.sendCmd(const.LG2LGATEM_REQUEST_CONFIG,
                         json.dumps({'server_ip':self.startconfig.server_ip,
                                 'server_port':self.startconfig.server_port
                                 }
                                ))
        elif self.starttype == START_TYPE_LOGINSERVER:
            self.sendCmd(const.L2LGATEM_REQUEST_CONFIG,
                         json.dumps({'server_ip': self.startconfig.server_ip,
                                     'server_port': self.startconfig.server_port
                                     }
                                    ))

    def packetReceived(self, cmd, pkt):
        if cmd in (const.LGATEM2L_REPLY_CONFIG,const.LGATEM2LG_REPLY_CONFIG):
            config = json.loads(pkt)
            if config[u"error"]==const.ERROR_OK:
                self.callback(self.isdaemon,config[u"id"])
                logging.debug(u"logingatemanager.packetReceived()")
        else:
            logging.warn(u"unknow cmd :%d",cmd)
instance = LogingateManager()

if __name__ == '__main__':
    pass