# encoding: utf-8

"""
@author: xiexiangwei
@software: PyCharm
@file: gameuser.py
@time: 2017/5/19 15:40
"""


class GameUser(object):
    def __init__(self, user_id, user_name, money, client):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__money = money
        self.__client = client

    def GetUserID(self):
        return self.__user_id

    def GetUserName(self):
        return self.__user_name

    def GetMoney(self):
        return self.money

    def GetClient(self):
        return self.client

    # 发消息给客户端
    def SendCmd(self, cmd, pkt):
        return self.__client.sendCmd(cmd, pkt)
