#coding=utf-8
import logging
from twisted.internet import task
import config
from common import redispool
import time

class RedisHelper(object):
    def __init__(self):
        self.redis_linkcount = config.instance.redis_linkcount if config.instance.redis_linkcount else 2
        self.__redispool = redispool.RedisConnectionPool(ip=config.instance.redis_ip,
                                                         port=config.instance.redis_port,
                                                         db=config.instance.redis_db,
                                                         password=config.instance.redis_pwd,
                                                         linkcount=self.redis_linkcount)

        #登录服务器列表
        self.__loginserverlist=[]
        self.time = 0

    def start(self):
        l = task.LoopingCall(self.OnTimer)
        l.start(1, False)
        self.__redispool.start()


    def OnTimer(self):
        self.LoadLoginServerList()
        print self.time

    def HashIndex(self, v):
        return int(v) % self.redis_linkcount

    #获取登录服务器信息列表
    def LoadLoginServerList(self):
        cmd = redispool.RedisCommand(index=self.HashIndex(time.time()),
                                     func=self.LoadLoginServerListFunc,
                                     params=(),
                                     ctx=(),
                                     finish=self.LoadLoginServerListFinish)
        self.__redispool.putCmd(cmd)

    def LoadLoginServerListFunc(self,redisclient):
        res = []
        loginserverid_list = redisclient.smembers(u"loginserver:loginserver_list")
        for loginserverid in loginserverid_list:
            key = u"loginserver:loginserver%s"%loginserverid
            if redisclient.exists(key):
                res.append(redisclient.hgetall(key))
            else:
                redisclient.srem(u"loginserver:loginserver_list",loginserverid)
        return res

    def LoadLoginServerListFinish(self,err,ctx,rows):
        self.__loginserverlist = rows

    #更新登录服务器使用次数
    def UpdateLoginServerTimes(self,id,value):
        cmd = redispool.RedisCommand(index=self.HashIndex(time.time()),
                                     func=self.UpdateLoginServerTimesFunc,
                                     params=(id,value),
                                     ctx=(),
                                     finish=self.UpdateLoginServerTimesFinish)
        self.__redispool.putCmd(cmd)


    def UpdateLoginServerTimesFunc(self,redisclient, id, value):
        self.time +=1
        loginserver_key = u"loginserver:loginserver%d" % id
        if redisclient.exists(loginserver_key):
            curtimes = int(redisclient.hget(loginserver_key, u"times"))
            redisclient.hset(loginserver_key, u"times", curtimes + value)
        else:
            redisclient.srem(u"loginserver:loginserver_list", id)

    def UpdateLoginServerTimesFinish(self,err,ctx,rows):
        pass


    def GetLoginServerList(self):
        return self.__loginserverlist


instance = RedisHelper()
