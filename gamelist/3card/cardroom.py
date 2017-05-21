# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:15
# @Author  : xiexiangwei:
# @File    : cardroom.py
# @Software: PyCharm

from twisted.internet import task
import cardtable


# 诈金花房间
class CardRoom(object):
    def __init__(self, roomconfig):
        self.roomindex = roomconfig.roomindex
        self.roomtype = roomconfig.roomtype  # 房间类型(底注1/底注2/底注3...)
        self.minmoney = roomconfig.minmoney  # 最小携带金钱
        self.maxmoney = roomconfig.maxmoney  # 最大携带金钱
        self.tablecount = roomconfig.tablecount  # 房间内桌子数量
        self.description = roomconfig.description  # 房间说明
        self.pagetablenum = 10  # 一页显示10张桌子信息
        self.tablelist = []  # 房间内的桌子列表
        self.tablemap = {}  # 房间内桌子map,为了快速查找到房间
        for i in range(self.tablecount):
            t = cardtable.CardTable(i, roomconfig.seatnum)
            self.tablelist.append(t)
            self.tablemap[i] = t

    def Start(self):
        lc = task.LoopingCall(self.OnTimer)
        lc.start(1, False)

    def OnTimer(self):
        for (_, table) in enumerate(self.tablelist):
            table.CheckUser()

    # 最大多少页桌子
    def GetMaxTablePage(self):
        return (self.tablecount + self.pagetablenum - 1) / self.pagetablenum

    # 获取一张某一页的桌子列表
    def GetTableListByPageIndex(self, page_index):
        return self.tablelist[page_index * self.pagetablenum:(page_index + 1) * self.pagetablenum]

    # 根据桌子索引获取桌子
    def GetTableByIndex(self, table_index):
        return self.tablemap.get(table_index)

    def UserEnter(self, user, table_index, seat_index):
        table = self.tablemap.get(table_index)

    def UserLeave(self, user):
        pass
