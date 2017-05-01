#coding=utf-8
from twisted.internet import task
import servermanager
import config
from common import const
import struct

class Robot(object):
    def __init__(self,id):
        self.id = id
        self.sm = None

    def start(self):
        l = task.LoopingCall(self.OnTimer())
        l.start(1,False)
        self.sm = servermanager.ServerManager(self)
        self.sm.start(config.instance)

    def OnTimer(self):
        pass

    def GetLoginGate(self):
        self.sm.sendCmd(const.C2SM_GET_LOGINGATE,struct.pack("H",0))

    def OnGetLoginGate(self,data):
        print data
