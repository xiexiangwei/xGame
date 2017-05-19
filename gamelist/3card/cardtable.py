# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:17
# @Author  : xiexiangwei
# @File    : cardtable.py
# @Software: PyCharm

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
