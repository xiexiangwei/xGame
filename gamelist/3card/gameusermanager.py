# encoding: utf-8

"""
@author: xiexiangwei
@software: PyCharm
@file: gameusermanager.py
@time: 2017/5/19 15:41
"""
import logging
import gameuser
import time
import cardconfig
from common import const
import gamecenter
from twisted.internet import task
import json


class GameUserManager(object):
    def __init__(self):
        self.__gameusermap = {}

    def Start(self):
        lc = task.LoopingCall(self.Timer)
        lc.start(1, False)

    def Timer(self):
        self.SyncMoney()

    def SyncMoney(self):
        now = time.time()
        syncuserlist = []
        # 同步符合条件的玩家金币到游戏中心
        for (_, user) in enumerate(self.__gameusermap):
            if now - user.GetLastSyncMoneyTime() > cardconfig.instance.syncmoneyinterval or user.GetMoneyChange() >= cardconfig.instance.syncmoneydiff:
                syncuserlist.append(dict(user_id=user.GetUserID(), money_changge=user.GetMoneyChange()))
                user.SetLastSyncMoneyTime(now)
                user.SetMoneyChange(0)
        # 分页同步减少服务器通信
        pagesize = cardconfig.instance.syncmoneypagesize
        maxpagenum = (len(syncuserlist) + pagesize - 1) / pagesize
        for n in range(maxpagenum):
            gamecenter.instance.sendCmd(const.TCS2GC_SYNC_USER_MONEY,
                                        json.dumps(dict(syncuserlist=syncuserlist[n * pagesize:(n + 1) * pagesize])))

    def AddGameUser(self, user_id, user_name, money, client):
        logging.debug(u"AddGameUser() user_id:%d user_name:%s money:%d", user_id, user_name, money)
        gu = gameuser.GameUser(user_id, user_name, money, client)
        self.__gameusermap[user_id] = gu

    def RemoveGameUser(self, user_id):
        logging.debug(u"RemoveGameUser() user_id:%d", user_id)
        self.__gameusermap.pop(user_id)

    def GetGameUser(self, user_id):
        return self.__gameusermap.get(user_id)


instance = GameUserManager()
