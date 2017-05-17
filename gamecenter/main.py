# coding:utf-8

import platform
import sys

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
from common import daemon, utils, const, servermanager
import clientfactory
import config
import random
import time
import redishelper


def MainStop():
    pass


def MainRun(isdaemon,id):
    random.seed(time.time())
    logging.getLogger().setLevel(config.instance.log_level)
    handler = TimedRotatingFileHandler(filename=config.instance.log_file, when='D', interval=1)
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

    # redishelper.instance.start()
    clientfactory.instance.start(config.instance.server_ip, config.instance.server_port, config.instance.max_client)
    logging.info(u"游戏中心服务器启动成功")


def StartRequest(isdaemon):
    config.instance.server_ip = utils.getExternalIP()
    servermanager.instance.start(const.CLIENT_TYPE_GAMECENTER,
                                 config.instance,
                                 MainRun,
                                 isdaemon)
    reactor.run()
    logging.info(u"游戏中心服务器停止运行")
    MainStop()


def Run():
    daemon.run(config.instance.server_pid, StartRequest)


if __name__ == "__main__":
    Run()
