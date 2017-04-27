#coding=utf-8
import logging
class ClientManager(object):
    def __init__(self):
        self.__logingate_id_pool = []
        self.__loginserver_id_pool = []

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

instance = ClientManager()




