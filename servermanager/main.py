#coding:utf8

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
import redishelper
import clientmanager

def MainStop():
    redishelper.instance.stop()

def MainRun(isdaemon):
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
    redishelper.instance.start()
    clientmanager.instance.start(config.instance)
    logging.info(u"服务器管理服务器启动成功!")
    reactor.run()
    logging.info(u"服务器管理服务器停止运行!")
    MainStop()


def run():
    daemon.run(config.instance.server_pid,MainRun)

if __name__ == "__main__":
    run()


