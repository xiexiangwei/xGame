# -*- coding: utf-8 -*-
# @Time    : 2017/05/17 0017 15:17
# @Author  : xiexiangwei
# @File    : cardtable.py
# @Software: PyCharm

# 诈金花桌子
class CardTable(object):
    def __init__(self, seatnum):
        self.seatnum = seatnum  # 座位数量
        self.usermap = {}  # 每个座位对应的玩家
