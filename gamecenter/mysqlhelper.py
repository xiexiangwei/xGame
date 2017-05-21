# encoding: utf-8

"""
@author: xiexiangwei
@software: PyCharm
@file: mysqlhelper.py
@time: 2017/5/17 23:44
"""

import config
from twisted.internet import task, reactor
import logging
from common import dbpool, CmdMessage_pb2, const
import usermanager
import gamemanager
import time


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

    def LoadUserData(self, client, account_id):
        self.query(self.hashIndex(account_id),
                   (client, account_id),
                   u"call p_load_user(%s)",
                   (account_id,),
                   self.LoadUserDataFinish)

    def LoadUserDataFinish(self, ctx, error, rows):
        client = ctx[0]
        account_id = ctx[1]
        logging.debug(u"LoadUserDataFinish() account_id:%s:%s  rows:%s", account_id, rows)
        reply = CmdMessage_pb2.RePly_Enter_GameCenter()
        reply.error = const.ERROR_OK
        if not error:
            if len(rows) == 1:
                # 玩家信息
                reply.user_info.user_id = rows[0][1]
                reply.user_info.user_name = rows[0][2]
                reply.user_info.money = rows[0][3]
                # 游戏中心游戏列表
                for (gtype, gamelist) in gamemanager.instance.GetGameMap().items():
                    gcount = len(gamelist)
                    if gcount > 0:
                        hashindex = reply.user_id % gcount
                        game = reply.game_list.add()
                        game.game_type = gtype
                        game.game_ip = gamelist[hashindex].ip
                        game.game_port = gamelist[hashindex].port

                usermanager.instance.AddUser(user_id=reply.user_info.user_id,
                                             user_name=reply.user_info.user_name,
                                             money=reply.user_info.money,
                                             client=client)
            else:
                reply.error = const.ERROR_USER_NOT_EXISTS
        else:
            reply.error = const.ERROR_SERVER
        client.send2client(const.GC2C_REPLY_ENTER_GC, reply.SerializeToString())

    def SyncUsersMoney(self, syncuserlist):
        struerslist = ""
        for n in range(len(syncuserlist)):
            struerslist += (str(syncuserlist[n][u"user_id"]) + u",")
            struerslist += (str(syncuserlist[n][u"money_change"]) + u";")

        self.query(self.hashIndex(time.time()),
                   (syncuserlist,),
                   u"call p_sync_users_money(%s)",
                   (struerslist,),
                   self.SyncUsersMoneyFinish)
        logging.debug(u"SyncUsersMoney() struerslist:%s", struerslist)


    def SyncUsersMoneyFinish(self,ctx, error, rows):
        syncuserlist = ctx[0]
        logging.debug(u"SyncUsersMoneyFinish() syncuserlist:%s error:%s rows:%s",syncuserlist,error,rows)
        if not error:
            for n in range(len(syncuserlist)):
                user_id = syncuserlist[n][u"user_id"]
                money_change = syncuserlist[n][u"money_change"]
                user = usermanager.instance.GetUser(user_id)
                if user:
                    user.UpdateMoney(money_change)

instance = MysqlHelper()

if __name__ == "__main__":
    instance.start()
    #instance.LoadUserData("clinet", 1)
    instance.SyncUsersMoney([dict(user_id=1,money_change=100),dict(user_id=2,money_change=1000)])

    reactor.run()
