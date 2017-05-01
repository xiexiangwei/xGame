#coding=utf-8
import redis
import logging
class RedisHelper(object):
    def __init__(self):
        self.redisclient = None

    def start(self,conf):
        self.redisclient = redis.StrictRedis(host=conf.redis_ip,
                                             port=conf.redis_port,
                                             db=conf.redis_db,
                                             password=conf.redis_pwd)
        logging.info(u"正在连接redis ip:%s port:%d",conf.redis_ip,conf.redis_port)
        self.redisclient.ping()
        logging.info(u"redis连接成功 ip:%s port:%d", conf.redis_ip, conf.redis_port)


instance = RedisHelper()
