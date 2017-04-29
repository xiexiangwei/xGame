#coding=utf-8
class Config(object):
    def __init__(self):
        self.server_ip = u""
        self.server_port = 3001
        self.server_pid = u"/tmp/logingate.pid"
        self.max_client = 500
        # 登录网关管理服务器地址(取服务器索引,取到之后立刻断开连接)
        self.logingatemanager_ip = u"127.0.0.1"
        self.logingatemanager_port = 1111

        self.log_file = u"loginserver.log"
        self.log_format = u"%(asctime)s %(levelname)s %(message)s"
        self.log_level = u"DEBUG"

        self.redis_ip = u"192.168.195.128"
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_pwd = u""


instance = Config()
