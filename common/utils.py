#coding=utf-8

import socket

def GetLocalIP():
    return socket.gethostbyname(socket.gethostname())  # 得到本地ip

def getExternalIP():
    ipList = socket.gethostbyname_ex(socket.gethostname())
    localip = GetLocalIP()
    for ip in ipList[2]:
        if ip and ip != localip:
            return ip

