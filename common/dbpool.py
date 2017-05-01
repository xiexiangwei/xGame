# coding:utf-8

import MySQLdb
import threading
import logging
import time
from twisted.internet import reactor


class DBPError(Exception):
    "Database pool Error"


class DBCommand(object):
    def __init__(self):
        pass

    def selectCon(self, linkcount):
        return 0

    def execute(self, con):
        pass

    def finish(self, error):
        pass


class KeepAliveCmd(DBCommand):
    def selectCon(self, linkcount):
        return 0

    def execute(self, con):
        c = con.cursor()
        sql = u"select 1+1"
        c.execute(sql)
        rows = c.fetchall()
        c.close()
        # logging.debug("KeepAliveCmd ret=%s", rows[0][0])

    def finish(self, error):
        pass


class QueryCmd(DBCommand):
    def __init__(self, conindex, ctx, sql, params, func):
        DBCommand.__init__(self)
        self.__conindex = conindex
        self.__ctx = ctx
        self.__sql = sql
        self.__params = params
        self.__func = func
        self.__rows = None

    def selectCon(self, linkcount):
        return self.__conindex

    def execute(self, con):
        c = con.cursor()
        c.execute(self.__sql, self.__params)
        self.__rows = c.fetchall()
        c.close()

    def finish(self, error):
        try:
            if error:
                self.__func(self.__ctx, error, None)
            else:
                self.__func(self.__ctx, None, self.__rows)
        except Exception:
            logging.exception(u"QueryCmd.finish()")
        finally:
            self.__ctx = None
            self.__sql = None
            self.__func = None
            self.__rows = None


class ExecuteCmd(DBCommand):
    def __init__(self, conindex, ctx, sql, params, func):
        DBCommand.__init__(self)
        self.__conindex = conindex
        self.__ctx = ctx
        self.__sql = sql
        self.__params = params
        self.__func = func
        self.__rowcount = None

    def selectCon(self, linkcount):
        return self.__conindex

    def execute(self, con):
        c = con.cursor()
        c.execute(self.__sql, self.__params)
        self.__rowcount = c.rowcount
        c.close()

    def finish(self, error):
        try:
            if error:
                self.__func(self.__ctx, error, 0)
            else:
                self.__func(self.__ctx, None, self.__rowcount)
        except Exception:
            logging.exception(u"ExecuteCmd.finish()")
        finally:
            self.__ctx = None
            self.__sql = None
            self.__func = None


class CallProcCmd(DBCommand):
    def __init__(self, conindex, ctx, proc, params, func):
        DBCommand.__init__(self)
        self.__conindex = conindex
        self.__ctx = ctx
        self.__proc = proc
        self.__params = params
        self.__func = func
        self.__sets = []

    def selectCon(self, linkcount):
        return self.__conindex

    def execute(self, con):
        c = con.cursor()
        c.callproc(self.__proc, self.__params)
        while True:
            rows = c.fetchall()
            if not c.nextset():
                break
            else:
                self.__sets.append(rows)
        c.close()

    def finish(self, error):
        try:
            if error:
                self.__func(self.__ctx, error, None)
            else:
                self.__func(self.__ctx, None, self.__sets)
        except Exception:
            logging.exception(u"CallProcCmd.finish()")
        finally:
            self.__ctx = None
            self.__proc = None
            self.__func = None
            self.__sets = None


class DBConnection(object):
    def __init__(self, index, queuesize):
        self.__index = index
        self.__queuesize = queuesize
        self.__db = ""
        self.__user = ""
        self.__passwd = ""
        self.__host = ""
        self.__port = 3306
        self.__charset = ""
        self.__con = None
        self.__toExit = False
        self.__thread = None
        self.__event = None
        self.__cmdlist = []
        self.__lock = None

    def start(self, db, user, passwd, host, port, charset):
        self.__db = db
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__port = port
        self.__charset = charset

        self.__event = threading.Event()
        self.__lock = threading.Lock()
        self.__thread = threading.Thread(target=self.svc)
        self.__thread.start()

    def stop(self):
        self.__toExit = True
        self.__thread.join()
        self.__thread = None
        self.__event = None
        self.__lock = None

    def getCharSet(self):
        return self.__charset

    # MySQLdb目前不支持参数化语句，小心SQL注入攻击
    def escapeString(self, strt):
        return self.__con.escape_string(strt)

    def putCmd(self, cmd):
        self.__lock.acquire()
        if len(self.__cmdlist) > self.__queuesize:
            self.__lock.release()
            reactor.callFromThread(cmd.finish, DBPError(u"mysqldb queue full"))
            return
        self.__cmdlist.append(cmd)
        self.__lock.release()
        self.__event.set()

    def svc(self):
        lastexecutetime = time.time()
        while not self.__toExit:
            if not self.__con:
                self.connect()
                if not self.__con:
                    i = 0
                    while i < 50 and not self.__toExit:
                        time.sleep(0.1)
                        i = i + 1
                    continue

            if not self.__event.wait(timeout=0.1):
                if time.time() - lastexecutetime > 10 * 60:
                    self.putCmd(KeepAliveCmd())
                continue

            cmd = None
            self.__lock.acquire()
            if len(self.__cmdlist) == 0:
                self.__lock.release()
                self.__event.clear()
                continue
            cmd = self.__cmdlist.pop(0)
            self.__lock.release()

            lastexecutetime = time.time()
            try:
                cmd.execute(self.__con)
            except Exception, e:
                reactor.callFromThread(cmd.finish, e)
                logging.exception(u"cmd.execute()")
                logging.error(u"cmd.excute exception, class=%s error=%s",
                              cmd.__class__,
                              e)
                self.checkConnect()
                continue

            reactor.callFromThread(cmd.finish, None)
        if self.__con:
            self.__con.close()
            self.__con = None
        logging.warn(u"DBConnection thread exit!!!")

    def checkConnect(self):
        try:
            self.__con.ping()
        except Exception, e:
            logging.exception(u"self.__con.ping()")
            logging.error(u"__con.ping() exception, error=%s", e)
            self.__con.close()
            self.__con = None

    def connect(self):
        try:
            self.__con = MySQLdb.connect(db=self.__db,
                                         user=self.__user,
                                         passwd=self.__passwd,
                                         host=self.__host,
                                         port=self.__port,
                                         charset=self.__charset,
                                         connect_timeout=5,
                                         read_timeout=60,
                                         use_unicode=True
                                         )
        except Exception:
            self.__con = None
            logging.exception(u"self.connect()")
        if self.__con:
            # MySQLdb默认autocommit是OFF
            self.__con.autocommit(True)
            self.__con.charset = self.__charset
            logging.warn(u"mysql %s:%d connected", self.__host, self.__port)


class DBConnectionPool(object):
    def __init__(self, db, user, passwd, host=u'127.0.0.1', port=3306, charset=u'utf8', linkcount=3, queuesize=256):
        self.__db = db
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__port = port
        self.__charset = charset
        self.__linkcount = linkcount
        self.__queuesize = queuesize

        self.__cons = []
        for i in range(linkcount):  # 线程池
            self.__cons.append(DBConnection(i, self.__queuesize))

    def start(self):
        for con in self.__cons:
            con.start(self.__db,
                      self.__user,
                      self.__passwd,
                      self.__host,
                      self.__port,
                      self.__charset)

    def stop(self):
        for con in self.__cons:
            con.stop()
        self.__cons = {}

    def getLinkCount(self):
        return self.__linkcount

    def getCharset(self):
        return self.__charset

    def putCmd(self, cmd):
        self.__cons[cmd.selectCon(self.__linkcount)].putCmd(cmd)

    def escapeString(self, srt):
        return self.__cons[0].escapeString(srt)

    def query(self, conindex, ctx, sql, params, func):
        self.putCmd(QueryCmd(conindex, ctx, sql, params, func))

    def execute(self, conindex, ctx, sql, params, func):
        self.putCmd(ExecuteCmd(conindex, ctx, sql, params, func))

    def call(self, conindex, ctx, proc, params, func):
        self.putCmd(CallProcCmd(conindex, ctx, proc, params, func))
