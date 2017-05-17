# coding=utf-8
from twisted.internet import task

import config
from common import redispool


class RedisHelper(object):
    def __init__(self):
        self.redis_linkcount = config.instance.redis_linkcount if config.instance.redis_linkcount else 2
        self.__redispool = redispool.RedisConnectionPool(ip=config.instance.redis_ip,
                                                         port=config.instance.redis_port,
                                                         db=config.instance.redis_db,
                                                         password=config.instance.redis_pwd,
                                                         linkcount=self.redis_linkcount)

    def start(self):
        l = task.LoopingCall(self.OnTimer)
        l.start(1, False)
        self.__redispool.start()

    def OnTimer(self):
        pass

    def HashIndex(self, v):
        return int(v) % self.redis_linkcount


instance = RedisHelper()
