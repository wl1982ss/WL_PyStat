# -*- coding: UTF-8 -*-
import subprocess
import logging
import os
import redis
import sys


# create logger
logger = logging.getLogger(__name__)

globalKey = "public"
globalInterface = "em3"
globalIpAddr = "192.168.1.107"
RdsDBCfg = []


def DumpExceptionMsg(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()

#获得网络OID
def GetInterface(flag):
    cmd = "snmpwalk -v2c -c %s %s ifDescr | grep '%s' |  awk -F' |::' '{print $2}'|awk -F'.' '{print $2}'" % (
    globalKey, globalIpAddr, globalInterface)

    ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    ret.wait()
    idx = ret.stdout.readline().strip()

    # logger.debug("return [%s]" % idx)

    if idx == "":
        logger.debug("cmd return empty string")
        return ""

    if flag == "ifIn":
        return "ifHCInOctets.%s" % idx
    else:
        return ""


def WriteToRedis(speed):
    try:
        hres = redis.Redis(host=RdsDBCfg.RdsDBHost, port=RdsDBCfg.RdsDBPort, db=RdsDBCfg.RdsDBIdx, socket_timeout=RdsDBCfg.RdsSocketTimeOut)
        a = hres.get('total_redirect_num')
        if a is None:
            a = 0
        SvrNum = int(a)

        for idx in range(1, SvrNum + 1):
            key = 'py_net_speed_%d' % (idx)
            hres.set(key, speed)

    except Exception as err:
        DumpExceptionMsg(err)


def get_net_data():
    cmd = "C:\\usr\\bin\\snmpwalk -v 2c -c public 192.168.1.107"
    print("你好")
    print(os.popen("ipconfig").read())
    os.system(cmd)
    '''
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print(result)
    result.wait()
    retlst = result.stdout.readline().strip()
    retlst = retlst.split()
    #if len(retlst) != 4:
    '''


if __name__ == "__main__":
    get_net_data()


