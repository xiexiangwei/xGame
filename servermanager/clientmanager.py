#coding=utf-8
import logging
import config

class CLoginGate(object):
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.usetimes=0

class CGameGate(object):
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port


class ClientManager(object):
    def __init__(self):
        self.__logingate_id_pool = []
        self.__loginserver_id_pool = []
        self.__gamegate_id_pool = []
        self.logingatemap={}
        self.gamegatemap={}

    def start(self):
        config.instance.max_logingate = config.instance.max_logingate if config.instance.max_logingate else 100
        config.instance.max_loginserver = config.instance.max_loginserver if config.instance.max_loginserver else 100
        config.instance.max_gamegate = config.instance.max_gamegate if config.instance.max_gamegate else 100

        logging.info(u"最大登录网关数量:%d", config.instance.max_logingate )
        logging.info(u"最大登录服务器数量:%d", config.instance.max_loginserver)
        logging.info(u"最大游戏网关数量:%d", config.instance.max_gamegate)

        for i in range( config.instance.max_logingate):
            self.__logingate_id_pool.append(i)
        for i in range( config.instance.max_loginserver):
            self.__loginserver_id_pool.append(i)
        for i in range(config.instance.max_loginserver):
            self.__gamegate_id_pool.append(i)

    def GetLogingateID(self):
        if len(self.__logingate_id_pool) > 0:
            return self.__logingate_id_pool.pop()
        return None

    def GetLoginServerID(self):
        if len(self.__loginserver_id_pool) > 0:
            return self.__loginserver_id_pool.pop()
        return None

    def GetGameGateID(self):
        if len(self.__gamegate_id_pool) > 0:
            return self.__gamegate_id_pool.pop()
        return None

    def AddLogingate(self,id,ip,port):
        logingate = CLoginGate(ip,port)
        self.logingatemap[id] = logingate

    def RemoveLogingate(self,id):
        self.logingatemap.pop(id)
        self.__logingate_id_pool.append(id)

    def RemoveLoginServer(self,id):
        self.__loginserver_id_pool.append(id)

    def AddGameGate(self,id,ip,port):
        gg = CGameGate(ip,port)
        self.gamegatemap[id] = gg

    def RemoveGameGate(self, id):
        self.__gamegate_id_pool.append(id)
        self.gamegatemap.pop(id)

    #分配一个网关信息
    def DisLoginGate(self, id):
        l = len(self.logingatemap)
        if l > 0:
            return self.logingatemap[int(id) % l]
        return None

instance = ClientManager()




