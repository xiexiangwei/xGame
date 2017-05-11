#coding:utf-8
#createby Mrxxw 2015年10月29日
import redis
import threading
from twisted.internet import reactor
import logging
import time


class RedisCommand(object):
    def __init__(self,index,func,params,ctx,finish):
        self.__index =index
        self.__func = func
        self.__params = params
        self.__finish = finish
        self.__ctx = ctx
        self.__res = None


    def excute(self,rediscon):
        self.__res = self.__func(rediscon,*self.__params)

    def finish(self,error):
        self.__finish(error,self.__ctx,self.__res)

    def getIndex(self):
        return  self.__index

class RedisConnection(object):

    def __init__(self,ip='192.168.1.100',port=6379,db=0,password=None):
        self.__ip = ip
        self.__port = port
        self.__db = db
        self.__passwd = password

        self.__pool = None
        self.__strictredis = None
        self.__exit = None
        self.__thread = None
        self.__event = None
        self.__lock = None
        self.__queue = []


    def start(self):
        self.__pool = redis.ConnectionPool(host=self.__ip,port=self.__port,db=self.__db,password=self.__passwd)
        self.__strictredis = redis.StrictRedis(connection_pool=self.__pool)
        try:
            self.__strictredis.ping()
        except(redis.exceptions.RedisError):
            logging.exception(u"redis connect failed %s:%d",self.__ip,self.__port)
            self.__strictredis = None
        if self.__strictredis:
            logging.info(u"redis connected %s:%d[%d]",self.__ip,self.__port,self.__db)
            self.__event = threading.Event()
            self.__lock = threading.Lock()
            self.__thread = threading.Thread(target=self.run)
            self.__thread.start()

    def connect(self):
        self.__pool = redis.ConnectionPool(host=self.__ip,port=self.__port,db=self.__db,password=self.__passwd)
        self.__strictredis = redis.StrictRedis(connection_pool=self.__pool)
        try:
            self.__strictredis.ping()
        except(redis.exceptions.RedisError):
            logging.exception(u"redis reconnect failed! %s:%d",self.__ip, self.__port)
            self.__strictredis = None
        if self.__strictredis:
            logging.warn(u"redis %s:%d reconnected", self.__ip, self.__port)


    def stop(self):
        self.__exit = True
        self.__thread.join()
        self.__thread = None
        self.__event = None
        self.__lock = None
        self.__queue = []

    def run(self):
        while not self.__exit:
            if not self.__strictredis:
                self.connect()
                i = 0
                while i<50 and not self.__exit:
                    time.sleep(0.1)
                    i = i + 1
                continue
            if not self.__event.wait(timeout=0.1):
                continue;
            cmd = None
            self.__lock.acquire()
            if len(self.__queue)==0:
                self.__lock.release()
                self.__event.clear()
                continue
            cmd = self.__queue.pop(0)
            self.__lock.release()
            try:
                cmd.excute(self.__strictredis)
            except Exception as e:
                if isinstance(e, redis.exceptions.ConnectionError):
                    self.connect()
                reactor.callFromThread(cmd.finish, e)
                continue
            reactor.callFromThread(cmd.finish,None)

    def getStrictRedis(self):
        return  self.__strictredis

    def getPipe(self):
        return self.__strictredis.pipeline()

    def putCmd(self,cmd):
        self.__queue.append(cmd)
        self.__event.set()


class RedisConnectionPool(object):
    def __init__(self, ip, port, db,password, linkcount=5):
        self.__ip = ip
        self.__port = port
        self.__db = db
        self.__passwd = password

        self.__cons = []
        for i in range(linkcount):  # 线程池
            self.__cons.append(RedisConnection(ip,port,db,password))

    def start(self):
        for con in self.__cons:
            con.start()

    def stop(self):
        for con in self.__cons:
            con.stop()
        self.__cons = {}

    def getCharset(self):
        return self.__charset

    def putCmd(self, cmd):
        self.__cons[cmd.getIndex()].putCmd(cmd)


if __name__ == "__main__":
    redispool = RedisConnectionPool(ip="192.168.1.6",
                                    port=6379,
                                    db=4,
                                    password="zhanghe",
                                    linkcount=10)
    redispool.start()

    def func(rediscon,ip,prot):
        print (ip,prot)
        rediscon.sadd(u"testset",time.time())

    def finesh(error,ctx,rows):
        print (ctx,error,rows)

    testcmd = RedisCommand(index=1,
                           func=func,
                           params=("127.0.0.1",1000),
                           ctx=(100,888,999),
                           finish=finesh)

    redispool.putCmd(testcmd)

    reactor.run()




