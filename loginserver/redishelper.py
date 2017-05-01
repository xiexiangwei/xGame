#coding=utf-8
import redis
import logging
from twisted.internet import task

class RedisHelper(object):
    def __init__(self):
        self.redisclient = None
        self.loginserver_id = None
        self.loginserver_ip = None
        self.loginserver_port = None

    def start(self,conf):
        l = task.LoopingCall(self.OnTimer)
        l.start(1, False)

        self.redisclient = redis.StrictRedis(host=conf.redis_ip,
                                             port=conf.redis_port,
                                             db=conf.redis_db,
                                             password=conf.redis_pwd)
        logging.info(u"正在连接redis ip:%s port:%d",conf.redis_ip,conf.redis_port)
        print(self.redisclient.ping())
        logging.info(u"redis连接成功 ip:%s port:%d", conf.redis_ip, conf.redis_port)

    def stop(self):
        if self.loginserver_id != None:
            pipeline = self.redisclient.pipeline()
            pipeline.srem(u"loginserver:loginserver_list",self.loginserver_id)
            loginserver_key = u"loginserver:loginserver%d" % self.loginserver_id
            pipeline.rem(loginserver_key)
            pipeline.execute()

    def OnTimer(self):
        if self.loginserver_id != None:
            pipeline = self.redisclient.pipeline()
            if not self.redisclient.sismember(u"loginserver:loginserver_list",self.loginserver_id):
                pipeline.sadd(u"loginserver:loginserver_list", self.loginserver_id)
            loginserver_key = u"loginserver:loginserver%d" % self.loginserver_id
            if not self.redisclient.exists(loginserver_key):
                new_loginserver = {u"id": self.loginserver_id, u"ip":  self.loginserver_ip, u"port":  self.loginserver_port, u"times": 0}
                pipeline.hmset(loginserver_key, new_loginserver)
            pipeline.expire(loginserver_key, 5)
            pipeline.execute()

    def AddLoginServer(self,id,ip,port):
        pipeline = self.redisclient.pipeline()
        pipeline.sadd(u"loginserver:loginserver_list",id)
        new_loginserver = {u"id":id,u"ip":ip,u"port":port,u"times":0}
        loginserver_key = u"loginserver:loginserver%d"%id
        pipeline.hmset(loginserver_key,new_loginserver)
        pipeline.expire(loginserver_key,5)
        pipeline.execute()
        self.loginserver_id = id
        self.loginserver_ip = ip
        self.loginserver_port = port



instance = RedisHelper()
