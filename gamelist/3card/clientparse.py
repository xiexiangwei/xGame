# coding=utf-8
from common import fprotocol, const, CmdMessage_pb2
import logging
import json
import gamecenter


def RequestEnterGame(client, pkt):
    request = CmdMessage_pb2.Request_Enter_Game()
    request.ParseFromString(pkt)
    data = dict(user_id=request.user_id, client_id=client.getId())
    # 验证玩家在游戏中心状态,验证成功返回玩家数据
    gamecenter.instance.sendCmd(const.TCS2GC_CHECK_USER,
                                json.loads(data))


__cmdTable = {
    const.C2TCS_REQUEST_ENTERGAME: RequestEnterGame,
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
