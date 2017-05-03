#coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
from common import fprotocol
import logging
import loginserverparse

class LoginServerFactory(ReconnectingClientFactory):
    def __init__(self,loginserver):
        ReconnectingClientFactory.maxDelay = 5
        self.loginserver = loginserver

    def buildProtocol(self, addr):
        logging.warn(u" LoginServer CONNECTED!!!")
        self.resetDelay()
        return  self.loginserver

    def startedConnecting(self, connector):
        logging.warn(u" LoginServer connecting!!!")

    def clientConnectionLost(self, connector, reason):
        logging.warn(u" LoginServer DOWN!!!")
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.warn(u" LoginServer connect FAIL!!!")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class LoginServer(fprotocol.FProtocol):
    def __init__(self,client):
        fprotocol.FProtocol.__init__(self)
        self.factory = LoginServerFactory(self)
        self.client = client

    def start(self,ip,port):
        reactor.connectTCP(ip,
                           port,
                           self.factory)

    def stop(self):
        pass

    def connectionMade(self):
        logging.warn(u"LoginServer.connectionMade()")
        fprotocol.FProtocol.reset(self)

    def connectionLost(self):
        pass

    def packetReceived(self, cmd, pkt):
        try:
            loginserverparse.parse(self, cmd, pkt)
        except Exception:
            logging.exception(u"LoginServer.parse() cmd=%d" % cmd)