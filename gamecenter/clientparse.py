# coding=utf-8
'''
Created on 2016年1月11日

@author: xxw
'''
import json
from common import fprotocol, const, CmdMessage_pb2
import logging
import gamemanager
import redishelper
import usermanager
import mysqlhelper


def GameRegister(clinet, pkt):
    data = json.loads(pkt)
    clinet.SetCType(data[u"servertype"])
    clinet.SetSId(data[u"serverid"])
    gamemanager.instance.AddGame(data[u"servertype"],
                                 data[u"serverid"],
                                 data[u"serverip"],
                                 data[u"serverport"])


def RequestEnterGameCenter(client, pkt):
    request = CmdMessage_pb2.Request_Enter_GameCenter()
    request.ParseFromString(pkt)
    logging.debug(u"RequestEnterGameCenter() account_id:%d token:%s", request.account_id, request.token)
    redishelper.instance.VerifyToken(client,
                                     request.account_id,
                                     request.token)


def CheckUser(client, pkt):
    data = json.loads(pkt)
    user_id = data[u"user_id"]
    client_id = data[u"client_id"]
    logging.debug(u"CheckUser() user_id:%d client_id:%d", user_id, client_id)
    reply = dict(error=const.ERROR_OK, clinet_id=client_id)
    user = usermanager.instance.GetUser(user_id)
    if user:
        if not user.GetGameState():  # 验证成功
            reply[u"user_name"] = user.GetUserName()
            reply[u"money"] = user.GetMoney()
        else:
            reply["error"] = const.ERROR_USER_IS_GAMING  # 玩家已经在游戏中
    else:
        reply["error"] = const.ERROR_USER_NOT_IN_GC  # 玩家不在游戏中心
    client.sendCmd(const.GC2TCS_CHECK_USER_RESULT, json.dumps(reply))


def UpdateUserGameState(client, pkt):
    data = json.loads(pkt)
    user_id = data[u"user_id"]
    game_state = data[u"game_state"]
    logging.debug(u"UpdateUserGameState() user_id:%d game_state:%d", user_id, game_state)
    user = usermanager.instance.GetUser(user_id)
    if user:
        user.SetGameState(game_state)
    else:
        logging.warn(u"UpdateUserGameState() user is offline! user_id:%d", user_id)


def SyncUserMoney(client, pkt):
    data = json.loads(pkt)
    syncuserlist = data[u"syncuserlist"]
    logging.debug(u"SyncUserMoney() syncuserlist:%s", syncuserlist)
    mysqlhelper.instance.SyncUsersMoney(syncuserlist)


__cmdTable = {
    const.TCS2GC_REGISTER: GameRegister,
    const.C2GC_REQUEST_ENTER_GC: RequestEnterGameCenter,
    const.TCS2GC_CHECK_USER: CheckUser,
    const.TCS2GC_UPDATE_USER_GAMESTATE: UpdateUserGameState,
    const.TCS2GC_SYNC_USER_MONEY: SyncUserMoney,
}


def parse(clinet, cmd, pkt):
    func = __cmdTable.get(cmd)
    if not func:
        raise fprotocol.FPError(u"unknow cmd=%d" % cmd)
    logging.debug(u"clientparse() cmd:%s", func.func_name)
    func(clinet, pkt)


if __name__ == '__main__':
    pass
