# coding=utf-8
import cardconfig
import cardroom
import logging


class ThreeCardServer(object):
    def __init__(self):
        self.__id = None
        # 房间map,索引房间类型
        self.__cardroomlist = []

    def start(self, id):
        self.__id = id
        try:
            for index, roomcfg in enumerate(cardconfig.instance.roomlist):
                room = cardroom.CardRoom(roomcfg)
                self.__cardroomlist.append(room)
                room.Start()
                logging.info(u"创建游戏房间 房间类型:%d 最小携带金币:%d 最大携带金币:%d 房间桌子数量:%d 桌子座位数量:%d",
                             roomcfg.roomtype,
                             roomcfg.minmoney,
                             roomcfg.maxmoney,
                             roomcfg.tablecount,
                             roomcfg.seatnum)
        except Exception as e:
            logging.error(u"%s", e.message)

    def GetId(self):
        return self.__id

    def GetCardRoomList(self):
        return self.__cardroomlist

    def GetRoomByIndex(self, room_index):
        for (_, room) in enumerate(self.__cardroomlist):
            if room.roomindex == room_index:
                return room
        return None


instance = ThreeCardServer()
