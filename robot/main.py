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
import config
import random
import time
import robotmanager


def MainStop():
    pass

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

    logging.info(u"机器人服务器启动成功")
    robotmanager.instance.start(1000)
    reactor.run()
    MainStop()


def run():
    daemon.run(config.instance.server_pid,MainRun)

if __name__ == "__main__":
    run()


