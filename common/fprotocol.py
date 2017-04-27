# coding=utf-8

from twisted.internet import protocol
import struct
import logging
import time

class FPError(Exception):
    "xGame Protocol Error"

class FProtocol(protocol.Protocol):
    def __init__(self):
        self.__buffer = ''
        self.__contime = time.time()
        self.__lastactivetime = time.time()

    def packetReceived(self, cmd, pkt):
        pass

    def getConTime(self):
        return self.__contime

    def getLastActiveTime(self):
        return self.__lastactivetime

    def dataReceived(self, data):
        logging.debug("dataReceived (%d)", len(data))
        self.__buffer += data
        self.__lastactivetime = time.time()
        try:
            self.__parseBuffer()
        except Exception:
            logging.exception(u"dataReceived()")
            self.abort()

    def __parseBuffer(self):
        blen = len(self.__buffer)
        while blen >= 4:
            plen, pcmd = struct.unpack("HH", self.__buffer[0:4])

            if blen < plen + 2:
                break

            pkt = self.__buffer[4:4 + plen - 2];
            self.__buffer = self.__buffer[plen + 2:]

            if pcmd > 0:
                self.packetReceived(pcmd, pkt)

            blen = len(self.__buffer)

    def sendPacket(self, data):
        self.transport.write(data)
        self.__lastactivetime = time.time()

    def sendCmd(self, cmd, data):
        head = struct.pack("HH", len(data) + 2, cmd)
        fmt = "%ds" % len(data)
        body = struct.pack(fmt, data)
        tail = struct.pack("H", 0)
        senddata = head + body + tail
        self.transport.write(senddata)
        self.__lastactivetime = time.time()

    def abort(self):
        self.transport.abortConnection()

    def reset(self):
        self.__buffer = ''

    def sendKeepAlive(self):
        self.sendPacket(struct.pack("H", 0))

    def isConnected(self):
        return self.connected
