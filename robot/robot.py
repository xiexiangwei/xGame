#coding=utf-8
from twisted.internet import task
import servermanager
import config
from common import const
import struct
import json
import logingate

class Robot(object):
    def __init__(self,id):
        self.id = id
        self.sm = servermanager.ServerManager(self)
        self.logingate = logingate.Logingate(self)

    def start(self):
        self.sm.start(config.instance)


    def GetLoginGate(self):
        self.sm.sendCmd(const.C2SM_GET_LOGINGATE,struct.pack("H",0))

    def OnGetLoginGate(self,data):
        logingate_info = json.loads(data)
        self.sm.abort()
        if logingate_info[u"error"] == const.ERROR_OK:
            print logingate_info
            self.logingate.start(logingate_info[u"ip"],logingate_info[u"port"])

    def Login(self):
        self.logingate.sendCmd(const.C2LG_Login,json.dumps({u"user_name":"robot_%d"%self.id,u"user_pwd":"123456"}))

