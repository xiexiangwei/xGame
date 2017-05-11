#coding:utf-8

import sys,platform
sys.path.append("../")
if 'twisted.internet.reactor' not in sys.modules:
    if platform.system() == "Linux":
        from twisted.internet import epollreactor
        epollreactor.install()
    else:
        from twisted.internet import iocpreactor
        iocpreactor.install()

import logging
from logging.handlers import TimedRotatingFileHandler
from twisted.internet import reactor
from twisted.python import log
from common import daemon
import clientfactory
import config
import random
import time
from common import servermanager,utils
import redishelper
import mysqlhelper



def MainStop():
    redishelper.instance.stop()
    mysqlhelper.instance.stop()

def MainRun(isdaemon,id):
    random.seed(time.time())
    logging.getLogger().setLevel(config.instance.log_level)
    handler = TimedRotatingFileHandler(filename=config.instance.log_file,when='D',interval=1)
    handler.setLevel(config.instance.log_level)
    formatter = logging.Formatter(config.instance.log_format)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    log.PythonLoggingObserver().start()
    if not isdaemon:
        handler = logging.StreamHandler()
        handler.setLevel(config.instance.log_level)
        formatter = logging.Formatter(config.instance.log_format)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

    #建立socket监听
    clientfactory.instance.start(config.instance.server_ip,config.instance.server_port,config.instance.max_client)
    #连接redis
    redishelper.instance.start()
    redishelper.instance.AddLoginServer(id,utils.getExternalIP(),config.instance.server_port)
    #连接mysql
    mysqlhelper.instance.start()

    logging.info(u"登录服务器启动成功!服务器ID:%u",id)


def GetLogingateConfig(isdaemon):
    config.instance.server_ip = utils.getExternalIP()
    servermanager.instance.startLoginServer(config.instance,
                                            MainRun,
                                            isdaemon)
    reactor.run()
    logging.info(u"登录服务器停止运行!服务器ID:%u",id)
    MainStop()

def run():
    daemon.run(config.instance.server_pid,GetLogingateConfig)

if __name__ == "__main__":
    run()


