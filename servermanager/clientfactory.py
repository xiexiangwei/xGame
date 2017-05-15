#coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''

from common import baseclientfactory,const
import client
import time

class ClientFactory(baseclientfactory.BaseClientFactory):

    def __init__(self):
        baseclientfactory.BaseClientFactory.__init__(self)

    def createClient(self, pid, addr):
        return client.Client(pid, addr)

    def getClient(self, pid):
        return self.getProtocol(pid)
    
    def checkClients(self, clients):
        curtime = time.time()

        for c in clients:
            if c.getState() == client.CLIENT_STATE_TO_CLOSE and curtime-c.toclosetime > 10:
                c.abort()
            elif curtime-c.getLastActiveTime() > 60:
                #如果是用戶socket，60秒內沒消息直接T掉
                if c.type == const.CLIENT_TYPE_USER:
                    c.abort()
                else:
                    c.sendKeepAlive()


instance = ClientFactory()
