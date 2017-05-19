# encoding: utf-8

"""
@author: xiexiangwei
@software: PyCharm
@file: usermanager.py
@time: 2017/5/18 0:00
"""
import logging
import user


class UserManager(object):
    def __init__(self):
        self.usermap = {}

    def AddUser(self, user_id, user_name, money, client):
        logging.debug(u"AddUser() user_id:%d user_name:%s money:%d", user_id, user_name, money)
        u = user.User(user_id, user_name, money, client)
        self.usermap[user_id] = u

    def GetUser(self, user_id):
        return self.usermap.get(user_id)


instance = UserManager()
