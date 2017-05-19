# coding=utf-8
import struct
from common import fprotocol, const, CmdMessage_pb2
import logging
import json
import clientfactory
import gameusermanager
import cardserver


def Keeplive(clinet, pkt):
    pass


def CheckUserResult(client, pkt):
    data = json.loads(pkt)
    error = data[u"error"]
    user_id = data[u"user_id"]
    client_id = data[u"client_id"]
    logging.debug(u"CheckUser() user_id:%d client_id:%d error:%d", user_id, client_id, error)
    user_clinet = clientfactory.instance.getClient(client_id)
    if user_clinet:
        reply = CmdMessage_pb2.Reply_Enter_Game()
        reply.error = error
        if reply.error == const.ERROR_OK:  # 验证成功
            user_name = data[u"user_name"]
            money = data[u"money"]
            # 玩家信息
            reply.user_info.user_id = user_id
            reply.user_info.user_name = user_name
            reply.user_info.money = money
            # 房间列表
            for (_, cardromm) in enumerate(cardserver.instance.GetCardRoomList()):
                room = reply.room_list.add()
                room.room_index = cardromm.roomindex
                room.room_type = cardromm.roomtype
                room.min_money = cardromm.minmoney
                room.max_money = cardromm.maxmoney
                room.table_count = cardromm.tablecount
                room.seat_num = cardromm.seatnum
                room.description = cardromm.description

            # 添加游戏玩家
            gameusermanager.instance.AddGameUser(user_id, user_name, money, user_clinet)
            # 更新游戏中心玩家状态
            client.sendCmd(const.TCS2GC_UPDATE_USER_GAMESTATE,
                           json.dumps(dict(user_id=user_id,
                                           game_state=True)))

        user_clinet.sendCmd(const.TCS2C_REPLY_ENTERGAME, reply.SerializeToString())
    else:
        logging.warn(u"CheckUserResult() user is offline! user_id:%d", user_id)


__cmdTable = {
    const.KEEPLIVE: Keeplive,
    const.GC2TCS_CHECK_USER_RESULT: CheckUserResult
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"gamecenter parse() func:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
