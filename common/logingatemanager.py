# coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
import logging
import fprotocol
import struct

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
        self.callback = None
        self.isdaemon = False

    def start(self, ip,port,callback,isdaemon):
        reactor.connectTCP(ip,port, LogingateManagerFactory())
        self.callback = callback
        self.isdaemon = isdaemon
    def stop(self):
        pass

    def connectionMade(self):
        logging.info(u"logingatemanager.connectionMade()")
        fprotocol.FProtocol.reset(self)
        self.sendCmd(1,struct.pack("HH",100,88))

    def packetReceived(self, cmd, pkt):
        logging.debug(u"logingatemanager.packetReceived()")

instance = LogingateManager()

if __name__ == '__main__':
    pass