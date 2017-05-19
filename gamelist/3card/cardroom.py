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
        self.tablecount = roomconfig.tablecount  # 房间内桌子数量
        self.description = roomconfig.description  # 房间说明
        self.pagetablenum = 10  # 一页显示10张桌子信息
        self.tablelist = []  # 房间内的桌子
        for i in range(self.tablecount):
            self.tablelist.append(cardtable.CardTable(i, roomconfig.seatnum))

    def GetMaxTablePage(self):
        # 一页10张桌子信息
        return self.tablecount / self.pagetablenum + 1

    # 获取一张某一页的桌子列表
    def GetTableListByPageIndex(self, page_index):
        return self.tablelist[page_index * self.pagetablenum:(page_index + 1) * self.pagetablenum]

    def UserEnter(self):
        pass

    def UserLeave(self):
        pass
