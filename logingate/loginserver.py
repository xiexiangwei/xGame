#coding=utf-8

from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from common import fprotocol
import logging
import loginserverparse

class LoginServerFactory(ClientFactory):
    def __init__(self, loginserver):
        self.loginserver = loginserver

    def buildProtocol(self, addr):
        logging.warn(u" LoginServer CONNECTED!!!")
        return self.loginserver

    def startedConnecting(self, connector):
        ClientFactory.startedConnecting(self, connector)
        logging.warn(u" LoginServer connecting!!!")

    def clientConnectionLost(self, connector, reason):
        ClientFactory.clientConnectionLost(self, connector, reason)
        logging.warn(u" LoginServer DOWN!!! reason:%s",reason)
        self.loginserver.onConnectionLost()

    def clientConnectionFailed(self, connector, reason):
        ClientFactory.clientConnectionFailed(self, connector, reason)
        logging.warn(u" LoginServer connect FAIL!!!")
        self.loginserver.connectionFail()


class LoginServer(fprotocol.FProtocol):
    def __init__(self,user):
        fprotocol.FProtocol.__init__(self)
        self.factory = LoginServerFactory(self)
        self.user = user

    def start(self,ip,port):
        reactor.connectTCP(ip,
                           port,
                           self.factory)

    def stop(self):
        pass

    def connectionMade(self):
        logging.warn(u"LoginServer.connectionMade()")
        fprotocol.FProtocol.reset(self)
        if self.user:
            self.user.ReadyToLogin(True)

    def connectionFail(self):
        logging.warn(u"LoginServer.connectionFail()")
        if self.user:
            self.user.ReadyToLogin(False)

    def onConnectionLost(self):
        logging.warn(u"LoginServer.onConnectionLost()")
        if self.user:
            self.user.ReadyToLogin(False)

    def packetReceived(self, cmd, pkt):
        try:
            loginserverparse.parse(self, cmd, pkt)
        except Exception:
            logging.exception(u"LoginServer.parse() cmd=%d" % cmd)
