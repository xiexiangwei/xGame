# encoding: utf-8

"""
@author: xiexiangwei
@software: PyCharm
@file: gameusermanager.py
@time: 2017/5/19 15:41
"""
import logging
import gameuser


class GameUserManager(object):
    def __init__(self):
        self.__gameusermap = {}

    def AddGameUser(self, user_id, user_name, money, client):
        logging.debug(u"AddGameUser() user_id:%d user_name:%s money:%d", user_id, user_name, money)
        gu = gameuser.GameUser(user_id, user_name, money, client)
        self.__gameusermap[user_id] = gu

    def GetGameUser(self, user_id):
        return self.__gameusermap.get(user_id)


instance = GameUserManager()
