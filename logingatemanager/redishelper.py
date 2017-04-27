import redis

class RedisHelper(object):
    def __init__(self):
        self.redisclient = None

    def start(self,conf):
        self.redisclient = redis.StrictRedis(host=conf.redis_ip,
                                             port=conf.redis_port,
                                             db=conf.redis_db,
                                             password=conf.redis_pwd)


instance = RedisHelper()
