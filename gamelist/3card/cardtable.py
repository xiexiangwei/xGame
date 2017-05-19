# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:17
# @Author  : xiexiangwei
# @File    : cardtable.py
# @Software: PyCharm

import logging

TABLE_STATE_GAMING = 1  # 正在游戏
TABLE_STATE_FREE = 2  # 空闲


# 诈金花桌子
class CardTable(object):
    def __init__(self, tableindex, seatnum):
        self.tableindex = tableindex  # 桌子索引
        self.seatnum = seatnum  # 座位数量
        self.usermap = {}  # 每个座位对应的玩家
        self.tablestate = TABLE_STATE_FREE  # 桌子游戏状态

    def GetTableIndex(self):
        return self.tableindex

    def GetSeatNum(self):
        return self.seatnum

    def GetUserMap(self):
        return self.usermap

    def GetTabelState(self):
        return self.tablestate

    # 根据座位号获取玩家
    def GetUserBySeatNum(self, seatnum):
        return self.usermap.get(seatnum)

    # 判断是否可以坐在当前座位上,返回座位号
    def CanSit(self, seatnum=None):
        seat = None
        if seatnum is not None:
            if not self.usermap.get(seatnum):
                seat = seatnum
        else:
            # 如果没指定座位则分配一个空闲座位
            for n in range(self.seatnum):
                if not self.usermap.get(n):
                    seat = n
                    break
        return seat

    # 广播信息给桌上所有玩家
    def Broadcast(self, cmd, pkt):
        logging.debug(u"Broadcast() cmd:%d", cmd)
        for (_, user) in enumerate(self.usermap):
            user.SendCmd(cmd, pkt)

    # 玩家坐进桌子
    def UserSit(self, user, seatnum):
        if not self.usermap.get(seatnum):
            self.usermap[seatnum] = user
        else:
            logging.error(u"UserSit() seat already has user! user_id:%d seatnum:%d", user.GetUserID(), seatnum)
