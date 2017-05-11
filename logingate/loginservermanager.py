#coding=utf-8

import redishelper

class LoginServerManager(object):
    def __init__(self):
        pass

    #分配登录服务器
    def DisLoginServer(self,pid):
        loginserver_list = redishelper.instance.GetLoginServerList()
        l = len(loginserver_list)
        if l > 0:
            return loginserver_list[pid % l ]
        return None


instance = LoginServerManager()