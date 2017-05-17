# coding=utf-8
import struct
from common import fprotocol, const
import logging
import json


def keeplive(clinet, pkt):
    pass


__cmdTable = {
    const.KEEPLIVE: keeplive,
}

def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"gamecenter parse() func:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
