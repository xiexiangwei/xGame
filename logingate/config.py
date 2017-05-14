#coding=utf-8
class Config(object):
    def __init__(self):
        self.server_ip = u""
        self.server_port = 2001
        self.max_client = 10000
        self.server_pid = u"/tmp/logingate.pid"

        #管理服务器地址
        self.servermanager_ip = u"127.0.0.1"
        self.servermanager_port = 1111

        self.log_file = u"logingate.log"
        self.log_format = u"%(asctime)s %(levelname)s %(message)s"
        self.log_level = u"DEBUG"

        self.redis_ip = u"192.168.195.128"
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_pwd = u""
        self.redis_linkcount = 10


instance = Config()
