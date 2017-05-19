# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:15
# @Author  : xiexiangwei:
# @File    : cardroom.py
# @Software: PyCharm

import cardtable


# 诈金花房间
class CardRoom(object):
    def __init__(self, roomconfig):
        self.roomindex = roomconfig.roomindex
        self.roomtype = roomconfig.roomtype  # 房间类型(底注1/底注2/底注3...)
        self.minmoney = roomconfig.minmoney  # 最小携带金钱
        self.maxmoney = roomconfig.maxmoney  # 最大携带金钱
        self.description = roomconfig.description  # 房间说明
        self.tablemap = {}  # 房间内的桌子
        for i in range(roomconfig.tablecount):
            self.tablemap[i] = cardtable.CardTable(roomconfig.seatnum)

    def UserEnter(self):
        pass

    def UserLeave(self):
        pass
