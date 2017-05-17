#coding=utf-8

class ThreeCardServer(object):
    def __int__(self):
        self.__id = None

    def start(self,id):
        self.__id = id

    def GetId(self):
        return  self.__id

instance = ThreeCardServer()