#coding=utf-8

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
from common import fprotocol,const,utils
import logging
import gamecenterparse
import config
import gamecenterbuild
import cardserver

class GameCenterFactory(ReconnectingClientFactory):
    def __init__(self):
        ReconnectingClientFactory.maxDelay = 5

    def buildProtocol(self, addr):
        self.resetDelay()
        return instance

    def startedConnecting(self, connector):
        logging.debug(u" GameCenter startedConnecting!!!")

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        logging.warn(u" GameCenter clientConnectionLost!!!")

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        logging.warn(u" GameCenter clientConnectionFailed!!!")


class GameCenter(fprotocol.FProtocol):
    def __init__(self):
        fprotocol.FProtocol.__init__(self)
        self.factory = GameCenterFactory()

    def start(self):
        reactor.connectTCP(config.instance.gamecenter_ip,
                           config.instance.gamecenter_port,
                           self.factory)

    def stop(self):
        pass

    def connectionMade(self):
        logging.debug(u"GameCenter.connectionMade()")
        fprotocol.FProtocol.reset(self)
        self.sendCmd(const.TCS2GC_REGISTER,gamecenterbuild.Register2GameCenter(const.CLIENT_TYPE_3CARD,
                                                         cardserver.instance.GetId(),
                                                         utils.getExternalIP(),
                                                         config.instance.server_port))

    def connectionFail(self):
        logging.warn(u"GameCenter.connectionFail()")


    def onConnectionLost(self):
        logging.warn(u"GameCenter.onConnectionLost()")


    def packetReceived(self, cmd, pkt):
        try:
            gamecenterparse.parse(self, cmd, pkt)
        except Exception:
            logging.exception(u"GameCenter.parse() cmd=%d" % cmd)


instance = GameCenter()