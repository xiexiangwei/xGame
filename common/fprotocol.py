# coding=utf-8

from twisted.internet import protocol
import struct
import time
from common import const

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
        self.__buffer += data
        self.__lastactivetime = time.time()
        try:
            self.__parseBuffer()
        except Exception:
            self.abort()

    def __parseBuffer(self):
        blen = len(self.__buffer)
        while blen >= 4:
            plen, pcmd = struct.unpack("HH", self.__buffer[0:4])

            if blen < plen + 2:
                break

            pkt = self.__buffer[4:4 + plen - 2];
            self.__buffer = self.__buffer[plen + 4:]

            if pcmd > 0:
                self.packetReceived(pcmd, pkt)

            blen = len(self.__buffer)


    def sendCmd(self, cmd, data):
        fmt = "%ds" % len(data)
        body = struct.pack(fmt, data)
        tail = struct.pack("H", 0)
        head = struct.pack("HH", len(data+tail), cmd)
        senddata = head + body + tail
        self.transport.write(senddata)
        self.__lastactivetime = time.time()

    def abort(self):
        self.transport.abortConnection()

    def reset(self):
        self.__buffer = ''

    def sendKeepAlive(self):
        self.sendCmd(const.KEEPLIVE,struct.pack("H",0))

    def isConnected(self):
        return self.connected
