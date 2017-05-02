#coding=utf-8
import redis
import logging
from twisted.internet import task

class RedisHelper(object):
    def __init__(self):
        self.redisclient = None

    def start(self,conf):
        l = task.LoopingCall(self.OnTimer)
        l.start(1, False)

        self.redisclient = redis.StrictRedis(host=conf.redis_ip,
                                             port=conf.redis_port,
                                             db=conf.redis_db,
                                             password=conf.redis_pwd)
        logging.info(u"正在连接redis ip:%s port:%d",conf.redis_ip,conf.redis_port)
        self.redisclient.ping()
        logging.info(u"redis连接成功 ip:%s port:%d", conf.redis_ip, conf.redis_port)


    def OnTimer(self):
        pass
        loginserver_list= self.GetLoginServerList()
        loginserver_list.sort(cmp=lambda x,y:cmp(int(x[u"times"]), int(y[u"times"])),reverse=False)

    #获取登录服务器信息列表
    def GetLoginServerList(self):
        res = []
        loginserverid_list = self.redisclient.smembers(u"loginserver:loginserver_list")
        for loginserverid in loginserverid_list:
            key = u"loginserver:loginserver%s"%loginserverid
            if self.redisclient.exists(key):
                res.append(self.redisclient.hgetall(key))
            else:
                self.redisclient.srem(u"loginserver:loginserver_list",loginserverid)
        return res


    #更新登录服务器使用次数
    def UpdateLoginServerTimes(self,id,value):
        loginserver_key = u"loginserver:loginserver%d" % id
        if self.redisclient.exists(loginserver_key):
            curtimes = int(self.redisclient.hget(loginserver_key,u"times"))
            self.redisclient.hset(loginserver_key, u"times",curtimes+value)
        else:
            self.redisclient.srem(u"loginserver:loginserver_list",id)


instance = RedisHelper()
