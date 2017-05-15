#coding=utf-8
import config
import redis
import logging
from twisted.internet import task
from common import redispool
import time

class RedisHelper(object):
    def __init__(self):
        self.redisclient = None
        self.loginserver_id = None
        self.loginserver_ip = None
        self.loginserver_port = None
        self.redis_linkcount = config.instance.redis_linkcount if config.instance.redis_linkcount else 2
        self.__redispool = redispool.RedisConnectionPool(ip=config.instance.redis_ip,
                                                         port=config.instance.redis_port,
                                                         db=config.instance.redis_db,
                                                         password=config.instance.redis_pwd,
                                                         linkcount=self.redis_linkcount)
    def start(self):
        l = task.LoopingCall(self.OnTimer)
        l.start(5, False)
        self.__redispool.start()


    def stop(self):
        self.RemoveLoginServer()
        while self.loginserver_id==None:
            self.__redispool.stop()

    def HashIndex(self, v):
        return int(v) % self.redis_linkcount

    def OnTimer(self):
        self.UpdateLoginServerExpireTime()

    #添加登录服务器到redis
    def AddLoginServer(self,id,ip,port):
        self.loginserver_id = id
        self.loginserver_ip = ip
        self.loginserver_port = port
        cmd = redispool.RedisCommand(index=self.HashIndex(time.time()),
                                     func=self.AddLoginServerFunc,
                                     params=(id,ip,port),
                                     ctx=(id,ip,port),
                                     finish=self.AddLoginServerFinish)
        self.__redispool.putCmd(cmd)

    def AddLoginServerFunc(self,redisclient,id,ip,port):
        redisclient.sadd(u"loginserver:loginserver_list", id)
        new_loginserver = {u"id": id, u"ip": ip, u"port": port, u"times": 0}
        loginserver_key = u"loginserver:loginserver%d" % id
        redisclient.hmset(loginserver_key, new_loginserver)
        redisclient.expire(loginserver_key, 10)

    def AddLoginServerFinish(self,error,ctx,rows):
        logging.info(u"AddLoginServerFinish() [%d] %s:%d",ctx[0],ctx[1],ctx[2])

    #更新登录服务器过期时间
    def UpdateLoginServerExpireTime(self):
        cmd = redispool.RedisCommand(index=self.HashIndex(time.time()),
                                     func=self.UpdateLoginServerExpireTimeFunc,
                                     params=(self.loginserver_id,self.loginserver_ip,self.loginserver_port),
                                     ctx=(self.loginserver_id,),
                                     finish=self.UpdateLoginServerExpireTimeFinish)
        self.__redispool.putCmd(cmd)

    def UpdateLoginServerExpireTimeFunc(self,redisclient,id,ip,port):
            if not redisclient.sismember(u"loginserver:loginserver_list", id):
                redisclient.sadd(u"loginserver:loginserver_list", id)
            loginserver_key = u"loginserver:loginserver%d" % id
            if not redisclient.exists(loginserver_key):
                new_loginserver = {u"id": id, u"ip": ip,u"port": port, u"times": 0}
                redisclient.hmset(loginserver_key, new_loginserver)
            redisclient.expire(loginserver_key, 10)

    def UpdateLoginServerExpireTimeFinish(self,error,ctx,rows):
        pass

    #从redis中删除登录服务器
    def RemoveLoginServer(self):
        if self.loginserver_id:
            cmd = redispool.RedisCommand(index=self.HashIndex(time.time()),
                                     func=self.RemoveLoginServerFunc,
                                     params=(self.loginserver_id),
                                     ctx=(self.loginserver_id,),
                                     finish=self.RemoveLoginServerFinish)
            self.__redispool.putCmd(cmd)

    def RemoveLoginServerFunc(self,redisclient,loginserver_id):
        redisclient.srem(u"loginserver:loginserver_list", loginserver_id)
        loginserver_key = u"loginserver:loginserver%d" % loginserver_id
        redisclient.rem(loginserver_key)

    def RemoveLoginServerFinish(self, error,ctx,rows):
        self.loginserver_id = None
        self.loginserver_ip = None
        self.loginserver_port = None

    #记录用户登录token
    def RecordAccountToken(self,account_id,token):
        cmd = redispool.RedisCommand(index=self.HashIndex(account_id),
                                 func=self.RecordAccountTokenFunc,
                                 params=(account_id,token),
                                 ctx=(account_id,token),
                                 finish=self.RecordAccountTokenFinish)
        self.__redispool.putCmd(cmd)

    def RecordAccountTokenFunc(self,redisclient,account_id,token):
        redisclient.sadd(u"accounttoken:accounttoken_list", account_id)
        token_key = u"accounttoken:accounttoken%d" % account_id
        redisclient.set(token_key,token)
        redisclient.expire(token_key,60*60*12)

    def RecordAccountTokenFinish(self, error,ctx,rows):
       logging.debug(u"RecordAccountTokenFinish() error:%s",error)




instance = RedisHelper()
