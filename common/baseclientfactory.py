# coding:utf-8

from twisted.internet import protocol, reactor, task
import logging


class BaseClientFactory(protocol.Factory):
    def __init__(self):
        # 可用id列表
        self.__idlist = []
        # 所有的protocol
        self.__pmap = {}

    def start(self, ip, port, maxclientcount, checkinterval=10):
        for i in range(maxclientcount):
            self.__idlist.append(i)
        reactor.listenTCP(port, self, interface=ip)
        l = task.LoopingCall(self.onTimer)
        l.start(checkinterval, False)

    def stop(self):
        pass

    def getClients(self):
        return self.__pmap.values()[:]

    def createClient(self, pid, addr):
        assert False, u"please override createClient()"

    def checkClients(self, clients):
        pass

    def buildProtocol(self, addr):
        if len(self.__idlist) == 0:
            logging.warn(u"server full")
            return None
        # 分配id
        pid = self.__idlist.pop(0)
        logging.debug(u"buildProtocol(), id=%d len(self.__pmap)=%d", pid, len(self.__pmap))
        p = self.createClient(pid, addr)
        self.__pmap[pid] = p
        return p

    def removeProtocol(self, prot):
        pid = prot.getId()
        p = self.__pmap.get(pid)
        if p != prot:
            logging.error(u"removeProtocol,  p!=protocol, id=%d", id)
            return
        self.__pmap.pop(pid)
        # 回收id
        self.__idlist.append(pid)
        logging.debug(u"removeProtocol(), id=%d len(self.__pmap)=%d", pid, len(self.__pmap))

    def getProtocol(self, pid):
        return self.__pmap.get(pid, None)

    def checkProtocol(self, proto):
        return self.getProtocol(proto.getId()) == proto

    def onTimer(self):
        clients = self.__pmap.values()[:]
        self.checkClients(clients)

    def broadcast(self, pkt):
        for c in self.__pmap.values():
            c.sendPacket(pkt)
