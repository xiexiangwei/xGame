# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:50
# @Author  : xiexiangwei
# @File    : cardconfig.py
# @Software: PyCharm

class RoomConfig(object):
    def __init__(self, rtype, minmoney, maxmoney, tablecount, seatnum):
        self.roomtype = rtype  # 房间类型(底注1/底注2/底注3...)
        self.minmoney = minmoney  # 最小携带金钱
        self.maxmoney = maxmoney  # 最大携带金钱(0表示不限制)
        self.tablecount = tablecount  # 房间内的桌子数量
        self.seatnum = seatnum  # 每张桌子座位数量


# 诈金花游戏配置
class CardGameConfig(object):
    def __init__(self):
        self.roomlist = []
        self.roomlist.append(RoomConfig(rtype=0, minmoney=1, maxmoney=1000, tablecount=1000, seatnum=4))
        self.roomlist.append(RoomConfig(rtype=1, minmoney=1000, maxmoney=5000, tablecount=500, seatnum=4))
        self.roomlist.append(RoomConfig(rtype=2, minmoney=5000, maxmoney=20000, tablecount=300, seatnum=4))
        self.roomlist.append(RoomConfig(rtype=3, minmoney=20000, maxmoney=0, tablecount=100, seatnum=4))


instance = CardGameConfig()
