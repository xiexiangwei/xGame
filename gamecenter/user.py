# encoding: utf-8

"""
@author: xiexiangwei
@software: PyCharm
@file: user.py
@time: 2017/5/18 0:00
"""


class User(object):
    def __init__(self, user_id, user_name, money, clinet):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__money = money
        self.__gamestate = False  # 用户的游戏状态 None:在游戏中心 true:游戏中
        self.__client = clinet

    def GetUserID(self):
        return self.__user_id

    def GetUserName(self):
        return self.__user_name

    def GetMoney(self):
        return self.__money

    def GetGameState(self):
        return self.__gamestate

    def GetClient(self):
        return self.__client

    def SetGameState(self, state):
        self.__gamestate = state

    def UpdateMoney(self, v):
        self.__money = self.__money + v if self.__money + v > 0 else 0
