# coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
import fprotocol
import const
import json

class ConfigException(Exception):
    "xGame Config Error"

class ServerManagerFactory(ReconnectingClientFactory):
    def __init__(self):
        ReconnectingClientFactory.maxDelay = 5

    def buildProtocol(self, addr):
        self.resetDelay()
        return instance

    def startedConnecting(self, connector):
        pass

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class ServerManager(fprotocol.FProtocol):
    def __init__(self):
        fprotocol.FProtocol.__init__(self)
        self.startconfig = None
        self.callback = None
        self.isdaemon = False
        self.servertype = None

    def start(self,type,conf,callback,isdaemon):
        if conf.servermanager_ip == None:
            raise ConfigException
        if conf.servermanager_port == None:
            raise ConfigException
        reactor.connectTCP(conf.servermanager_ip,
                           conf.servermanager_port,
                           ServerManagerFactory())
        self.startconfig = conf
        self.callback = callback
        self.isdaemon = isdaemon
        self.servertype = type

    def stop(self):
        pass

    def connectionMade(self):
        fprotocol.FProtocol.reset(self)
        data = dict(server_ip=self.startconfig.server_ip,
                    server_port=self.startconfig.server_port,
                    server_type = self.servertype)
        self.sendCmd(const.S2SM_REQUEST_START, json.dumps(data))


    def packetReceived(self, cmd, pkt):
        if cmd == const.SM2S_START_REPLY:
            config = json.loads(pkt)
            if config[u"error"]==const.ERROR_OK:
                self.callback(self.isdaemon,config[u"id"])
            else:
                print (u"开启服务器数量达到上限!")

instance = ServerManager()

if __name__ == '__main__':
    pass