#coding=utf-8
import logging

class CLoginGate(object):
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.usetimes=0


class ClientManager(object):
    def __init__(self):
        self.__logingate_id_pool = []
        self.__loginserver_id_pool = []
        self.logingatemap={}

    def start(self,conf):
        if conf.max_logingate == None:
            logging.error(u"没有配置最大登录网关数量")
        if conf.max_loginserver == None:
            logging.error(u"没有配置最大登录服务器数量")
        logging.info(u"最大登录网关数量:%d",conf.max_logingate )
        logging.info(u"最大登录服务器数量:%d",conf.max_loginserver)
        for i in range(conf.max_logingate):
            self.__logingate_id_pool.append(i)
        for i in range(conf.max_loginserver):
            self.__loginserver_id_pool.append(i)

    def GetLogingateID(self):
        if len(self.__logingate_id_pool) > 0:
            return self.__logingate_id_pool.pop()
        return None

    def GetLoginServerID(self):
        if len(self.__loginserver_id_pool) > 0:
            return self.__loginserver_id_pool.pop()
        return None

    def AddLogingate(self,id,ip,port):
        logingate = CLoginGate(ip,port)
        self.logingatemap[id] = logingate

    def RemoveLogingate(self,id):
        self.logingatemap.pop(id)
        self.__logingate_id_pool.append(id)

    def RemoveLoginServer(self,id):
        self.__loginserver_id_pool.append(id)

    #获取一个空闲网关信息
    def GetFreeLoginGate(self):
        if len(self.logingatemap) > 0:
            sorted_res = sorted(self.logingatemap.values(), lambda x, y:cmp(x.usetimes, y.usetimes),reverse=False)
            sorted_res[0].usetimes +=1
            return sorted_res[0]
        return None

instance = ClientManager()




