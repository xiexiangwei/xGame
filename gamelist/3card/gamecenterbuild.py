import logging
import json

def Register2GameCenter(servertype,serverid,serverip,serverport):
    logging.debug(u"Register2GameCenter() servertype:%d serverid:%d",servertype,serverid)
    return json.dumps(dict(servertype=servertype,
                           serverid=serverid,
                           serverip=serverip,
                           serverport=serverport))