# coding=utf-8

import logging


class Game(object):
    def __init__(self, stype, sid, sip, sport):
        self.type = stype
        self.id = sid
        self.ip = sip
        self.port = sport


class GameManager(object):
    def __init__(self):
        self.gamemap = {}

    def AddGame(self, stype, sid, sip, sport):
        logging.debug(u"AddGame() type:%d id:%d ip:%s port:%d", stype, sid, sip, sport)
        try:
            game = Game(stype, sid, sip, sport)
            if not self.gamemap.get(stype):
                self.gamemap[stype] = []
            self.gamemap[stype].append(game)
        except Exception as e:
            logging.error(u"AddGame() reason:%s", e.message)

    def RemoveGame(self, stype, sid):
        logging.warn(u"RemoveGame() type:%d id:%d ", stype, sid)
        gslist = self.gamemap.get(stype)
        if gslist:
            for index, gs in enumerate(gslist):
                if gs.id == sid:
                    gslist.pop(index)
                    break


instance = GameManager()
