# coding=utf-8
from common import fprotocol, const, CmdMessage_pb2
import logging
import json
import gamecenter
import cardserver


def RequestEnterGame(client, pkt):
    request = CmdMessage_pb2.Request_Enter_Game()
    request.ParseFromString(pkt)
    data = dict(user_id=request.user_id, client_id=client.getId())
    logging.debug(u"RequestEnterGame() user_id:%d", request.user_id)
    # 验证玩家在游戏中心状态,验证成功返回玩家数据
    gamecenter.instance.sendCmd(const.TCS2GC_CHECK_USER,
                                json.loads(data))


def RequestRoomTablesInfo(client, pkt):
    request = CmdMessage_pb2.Request_Room_Tables_Info()
    request.ParseFromString(pkt)
    logging.debug(u"RequestRoomTablesInfo() room_index:%d table_page:%d", request.room_index, request.table_page)
    user_id = client.GetUserID()
    reply = CmdMessage_pb2.Reply_Room_Tables_Info()
    reply.error = const.ERROR_OK
    if user_id:
        room_index = request.room_index
        table_page = request.table_page
        cardroom = cardserver.instance.GetRoomByIndex(room_index)
        if cardroom:
            if 0 <= table_page <= cardroom.GetMaxTablePage():
                reply.table_page = table_page
                # 获取该页桌子列表
                tablelist = cardroom.GetTableListByPageIndex(table_page)
                for (_, tableinfo) in enumerate(tablelist):
                    cardtable = reply.table_list.add()
                    cardtable.table_index = tableinfo.GetTableIndex()  # 桌子索引
                    cardtable.table_state = tableinfo.GetTabelState()  # 桌子状态
                    cardtable.table_seat_count = tableinfo.GetSeatNum()  # 桌子座位数量
                    for n in range(tableinfo.GetSeatNum()):
                        user = tableinfo.GetUserBySeatNum(n)
                        if user:
                            tableuser = cardtable.table_user_list.add()
                            tableuser.user_id = user.GetUserID()  # 玩家ID
                            tableuser.user_name = user.GetUserName()  # 玩家昵称
                            tableuser.seat_index = n  # 玩家座位号
            else:
                # 请求页数不正确
                reply.error = const.ERROR_INVALID_TABLE_PAGE
        else:
            # 请求房间索引不正确
            reply.error = const.ERROR_INVALID_ROOM_INDEX
    else:
        # 非法请求,断开连接
        reply.error = const.ERROR_INVALID_REQUEST
        client.kick()
    client.sendCmd(const.C2TCS_REPLY_ROOM_TABLES_INFO, reply.SerializeToString())


__cmdTable = {
    const.C2TCS_REQUEST_ENTERGAME: RequestEnterGame,
    const.C2TCS_REQUEST_ROOM_TABLES_INFO: RequestRoomTablesInfo,
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
