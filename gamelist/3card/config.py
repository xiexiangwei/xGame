# coding=utf-8
class Config(object):
    def __init__(self):
        self.server_ip = u""
        self.server_port = 40003
        self.max_client = 10000
        self.server_pid = u"/tmp/3card.pid"

        # 管理服务器地址
        self.servermanager_ip = u"127.0.0.1"
        self.servermanager_port = 1111

        # 游戏中心服务器地址
        self.gamecenter_ip = u"127.0.0.1"
        self.gamecenter_port = 8001

        self.log_file = u"3card.log"
        self.log_format = u"%(asctime)s %(levelname)s %(message)s"
        self.log_level = u"DEBUG"

        self.redis_ip = u"192.168.195.128"
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_pwd = u""
        self.redis_linkcount = 10


instance = Config()
