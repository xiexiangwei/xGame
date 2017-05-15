#coding=utf-8

import config
from twisted.internet import task
import logging
from common import dbpool,CmdMessage_pb2,const
import time
import base64
import redishelper

class MysqlHelper(object):
    def __init__(self):
        self.linkcount = 0
        self.dbp = None
        self.insertIndex = 0
        self.lastFinishOrderId = 0
        self.lastGiveMoneyId = 0

    def start(self):
        l = task.LoopingCall(self.onTimer)
        l.start(1, False)

        self.linkcount = config.instance.db_linkcount
        self.dbp = dbpool.DBConnectionPool(db=config.instance.db_name,
                                           user=config.instance.db_user,
                                           passwd=config.instance.db_pwd,
                                           host=config.instance.db_host,
                                           port=config.instance.db_port,
                                           linkcount=config.instance.db_linkcount)
        self.dbp.start()

    def stop(self):
        self.dbp.stop()

    def onTimer(self):
        self.doTask()

    def doTask(self):
        pass

    def hashIndex(self, value):
        return int(value) % self.linkcount

    def query(self, conindex, ctx, sql, params, func):
        self.dbp.query(conindex, ctx, sql, params, func)

    def execute(self, conindex, ctx, sql, params, func):
        self.dbp.execute(conindex, ctx, sql, params, func)


    def Login(self,client,account_name,account_pwd):
        self.query(self.hashIndex(time.time()),
                   (client,account_name,account_pwd),
                   u"call p_login(%s,%s)",
                   (account_name,account_pwd),
                   self.LoginFinish)

    def LoginFinish(self,ctx,error,rows):
        client = ctx[0]
        account_name = ctx[1]
        account_pwd = ctx[2]
        logging.debug(u"LoginFinish() account:%s:%s  rows:%s",account_name,account_pwd,rows)
        reply = CmdMessage_pb2.Reply_Login()
        reply.error = const.ERROR_OK
        if not error:
            res = rows[0]
            if res[0]==0:
                logging.debug(u"LoginFinish() success! %s:%s",account_name,account_pwd)
                token = base64.b32encode(u"%d-%f"%(reply.account_id,time.time()))
                reply.account_id = res[1]
                reply.token =token
                #记录到redis,提供游戏服务器查询
                redishelper.instance.RecordAccountToken(reply.account_id,token)
            elif res[0]==1:
                logging.debug(u"LoginFinish() account not exists! %s:%s", account_name, account_pwd)
                reply.error = const.ERROR_ACCOUNT_NOT_EXISTS
            elif res[0] == 2:
                logging.debug(u"LoginFinish() password is wrong! %s:%s", account_name, account_pwd)
                reply.error = const.ERROR_ACCOUNT_PWD_ERROR
        else:
            reply.error = const.ERROR_SERVER
        client.send2client(const.LG2C_LOGIN_RESULT, reply.SerializeToString())


instance = MysqlHelper()
