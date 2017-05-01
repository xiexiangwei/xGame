#coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
from common import fprotocol
import logging
import loginserverparse



class LoginServerFactory(ReconnectingClientFactory):
    def __init__(self):
        ReconnectingClientFactory.maxDelay = 5

    def buildProtocol(self, addr):
        logging.warn(u" LoginServer CONNECTED!!!")
        self.resetDelay()

    def startedConnecting(self, connector):
        logging.warn(u" LoginServer connecting!!!")

    def clientConnectionLost(self, connector, reason):
        logging.warn(u" LoginServer DOWN!!!")
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.warn(u" LoginServer connect FAIL!!!")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class LoginServer(fprotocol.FProtocol):
    def __init__(self):
        fprotocol.FProtocol.__init__(self)
        self.id=None
        self.callback=None

    def start(self,id,ip,port,callback):
        reactor.connectTCP(ip,
                           port,
                           LoginServerFactory())
        self.id=id
        self.callback =callback

    def stop(self):
        pass

    def connectionMade(self):
        logging.warn(u"LoginServer.connectionMade()")
        fprotocol.FProtocol.reset(self)
        self.callback(True,self)

    def connectionLost(self):
        self.callback(False,self)

    def packetReceived(self, cmd, pkt):
        try:
            loginserverparse.parse(self, cmd, pkt)
        except Exception:
            logging.exception(u"LoginServer.parse() cmd=%d" % cmd)