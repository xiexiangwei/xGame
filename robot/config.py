#coding=utf-8
class Config(object):
    def __init__(self):
        self.robot_num = 500
        self.server_pid = u"/tmp/robot.pid"
        # 登录网关管理服务器地址(取服务器索引,取到之后立刻断开连接)
        self.servermanager_ip = u"127.0.0.1"
        self.servermanager_port = 1111

        self.log_file = u"robot.log"
        self.log_format = u"%(asctime)s %(levelname)s %(message)s"
        self.log_level = u"DEBUG"



instance = Config()
