# coding=utf-8
from twisted.internet import task

import config
from common import redispool, CmdMessage_pb2, const
import logging


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

    # 验证token是否有效
    def VerifyToken(self, client, account_id, token):
        cmd = redispool.RedisCommand(index=self.HashIndex(account_id),
                                     func=self.VerifyTokenFunc,
                                     params=(account_id, token),
                                     ctx=(client, account_id, token),
                                     finish=self.VerifyTokenFinish)
        self.__redispool.putCmd(cmd)

    def VerifyTokenFunc(self, redisclient, account_id, token):
        ret = 0
        if redisclient.sismember(u"accounttoken:accounttoken_list", account_id):
            token_key = u"accounttoken:accounttoken%d" % account_id
            if redisclient.exists(token_key):
                r_token = redisclient.get(token_key)
                if r_token != token:
                    ret = 1  # token不相等
            else:
                redisclient.srem(u"accounttoken:accounttoken_list", account_id)
                ret = 2  # token不存在
        return ret

    def VerifyTokenFinish(self, error, ctx, rows):
        clinet = ctx[0]
        account_id = ctx[1]
        token = ctx[2]
        res = rows[0]
        logging.debug(u"VerifyTokenFinish() account_id:%d token:%s res:%d", account_id, token, res)
        if error or res != const.ERROR_OK:
            reply = CmdMessage_pb2.RePly_Enter_GameCenter()
            reply.error = const.ERROR_ACCOUNT_TOKEN_INVALID
            clinet.sendCmd(const.SM2C_GET_GAMECENTER_REPLY, reply.SerializeToString())
        else:
            pass


instance = RedisHelper()
