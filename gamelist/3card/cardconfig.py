# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:50
# @Author  : xiexiangwei
# @File    : cardconfig.py
# @Software: PyCharm

class RoomConfig(object):
    def __init__(self, index, rtype, minmoney, maxmoney, tablecount, seatnum, description):
        self.roomindex = index  # 房间索引
        self.roomtype = rtype  # 房间类型(底注1/底注2/底注3...)
        self.minmoney = minmoney  # 最小携带金钱
        self.maxmoney = maxmoney  # 最大携带金钱(0表示不限制)
        self.tablecount = tablecount  # 房间内的桌子数量
        self.seatnum = seatnum  # 每张桌子座位数量
        self.description = description  # 房间说明


# 诈金花游戏配置
class CardGameConfig(object):
    def __init__(self):
        self.roomlist = []
        self.roomlist.append(RoomConfig(index=0, rtype=0, minmoney=1, maxmoney=1000, tablecount=1000, seatnum=4, description=u"底注1房间"))
        self.roomlist.append(RoomConfig(index=1, rtype=1, minmoney=1000, maxmoney=5000, tablecount=500, seatnum=4, description=u"底注2房间"))
        self.roomlist.append(RoomConfig(index=2, rtype=2, minmoney=5000, maxmoney=20000, tablecount=300, seatnum=4, description=u"底注3房间"))
        self.roomlist.append(RoomConfig(index=3 ,rtype=3, minmoney=20000, maxmoney=0, tablecount=100, seatnum=4, description=u"底注4房间"))

        self.syncmoneyinterval = 5  # 定时同步金币到游戏中心时间间隔
        self.syncmoneydiff = 100  # 当金币变化大于等于n时同步金币到游戏中心
        self.syncmoneypagesize = 50  # 每次同步玩家金币一页玩家个数(主要为了减少服务器通讯次数)

instance = CardGameConfig()
