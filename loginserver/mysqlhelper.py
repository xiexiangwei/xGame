#coding=utf-8

import config
from twisted.internet import task
import logging
from common import dbpool

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
        return value % self.linkcount

    def query(self, conindex, ctx, sql, params, func):
        self.dbp.query(conindex, ctx, sql, params, func)

    def execute(self, conindex, ctx, sql, params, func):
        self.dbp.execute(conindex, ctx, sql, params, func)

instance = MysqlHelper()
