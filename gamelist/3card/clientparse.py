# coding=utf-8
from common import fprotocol, const, CmdMessage_pb2
import logging
import json
import gamecenter
import cardserver
import gameusermanager


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
    client.sendCmd(const.TCS2C_REPLY_ROOM_TABLES_INFO, reply.SerializeToString())


def RequestSit(client, pkt):
    request = CmdMessage_pb2.Request_Sit()
    request.ParseFromString(pkt)
    user_id = client.GetUserID()
    reply = CmdMessage_pb2.Reply_Sit()
    reply.error = const.ERROR_OK
    if user_id:
        logging.debug(u"RequestSit() user_id:%d room_index:%d table_index:%d seat_index:%d",
                      user_id,
                      request.room_index,
                      request.table_index,
                      request.seat_index if request.seat_index else -1,
                      )
        user = gameusermanager.instance.GetGameUser(user_id)
        if user:
            pass
            cardroom = cardserver.instance.GetRoomByIndex(request.room_index)
            if cardroom:
                table = cardroom.GetTableByIndex(request.table_index)
                if table:
                    validseat = table.CanSit(request.seat_index)
                    if validseat:
                        # 发送客户端消息逻辑
                        reply.room_index = request.room_index  # 房间索引
                        reply.table_index = request.table_index  # 桌子索引
                        reply.seat_index = request.validseat  # 座位索引
                        for n in range(table.GetSeatNum()):
                            user = table.GetUserBySeatNum(n)
                            if user:
                                tableuser = reply.user_list.add()
                                tableuser.user_id = user.GetUserID()  # 玩家ID
                                tableuser.user_name = user.GetUserName()  # 玩家昵称
                                tableuser.money = user.GetMoney()  # 玩家金币数量
                                tableuser.seat_index = n  # 玩家座位号
                        # 广播给桌子上所有玩家
                        bromsg = CmdMessage_pb2.Broadcast_User_Sit()
                        bromsg.new_user.user_id = user.GetUserID()  # 新加入玩家ID
                        bromsg.new_user.user_name = user.GetUserName()  # 新加入玩家昵称
                        bromsg.new_user.money = user.GetMoney()  # 新加入玩家金币数量
                        bromsg.new_user.seat_index = validseat  # 新加入玩家座位号
                        table.Broadcast(const.TCS2C_BROADCAST_USER_SIT, bromsg.SerializeToString())
                        # 服务器逻辑
                        cardroom.UserEnter(user, request.table_index, validseat)
                    else:
                        # 当前位子有人、没有空闲座位
                        reply.error = const.ERROR_INVALID_TABLE_INDEX
                else:
                    # 桌子索引不正确
                    reply.error = const.ERROR_INVALID_TABLE_INDEX
            else:
                # 请求房间索引不正确
                reply.error = const.ERROR_INVALID_ROOM_INDEX
        else:
            # 玩家不存在
            reply.error = const.ERROR_INVALID_REQUEST
            client.kick()
    else:
        # client没有设置user_id
        reply.error = const.ERROR_INVALID_REQUEST
        client.kick()
    client.sendCmd(const.TCS2C_REPLY_SIT, reply.SerializeToString())


__cmdTable = {
    const.C2TCS_REQUEST_ENTERGAME: RequestEnterGame,
    const.C2TCS_REQUEST_ROOM_TABLES_INFO: RequestRoomTablesInfo,
    const.C2TCS_REQUEST_SIT: RequestSit,
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
