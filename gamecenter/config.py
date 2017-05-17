#coding=utf-8
class Config(object):
    def __init__(self):
        self.server_ip = u""
        self.server_port = 6000
        self.max_client = 10000
        self.server_pid = u"/tmp/gamecenter.pid"

        #管理服务器地址
        self.servermanager_ip = u"127.0.0.1"
        self.servermanager_port = 1111

        self.log_file = u"gamecenter.log"
        self.log_format = u"%(asctime)s %(levelname)s %(message)s"
        self.log_level = u"DEBUG"

        self.redis_ip = u"192.168.195.128"
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_pwd = u""
        self.redis_linkcount = 1

        self.db_name = u"xGame-Game"
        self.db_host = u"192.168.195.128"
        self.db_port = 3306
        self.db_user = u"root"
        self.db_pwd = u"123456"
        self.db_linkcount = 2


instance = Config()
