#coding=utf-8

import redishelper

class LoginServerManager(object):
    def __init__(self):
        pass

    #获取一个空闲的登录服务器ID
    def GetFreeLoginServerID(self):
        loginserver_list = redishelper.instance.GetLoginServerList()
        if len(loginserver_list) > 0:
            loginserver_list.sort(cmp=lambda x, y: cmp(int(x[u"times"]), int(y[u"times"])), reverse=False)
            return loginserver_list[0]
        return None



instance = LoginServerManager()