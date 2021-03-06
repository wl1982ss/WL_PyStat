# -*- coding: UTF-8 -*-

import re
import os
import platform
import time


if 'Windows' == platform.system():
    hosts = ['192.168.1.107']
else:
    hosts = ['192.168.1.119']


def snmpWalk(host, oid):
    cmd = 'snmpwalk -v 2c -c public ' + host + ' ' + oid
    print(cmd)
    #result = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:1]
    result = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read()
    print(result)
    return result


def getSystem(host):
    #system = ':'.join(snmpWalk(host, 'system')[0].split(':')[3:]).strip()
    system = snmpWalk(host, 'system')
    return system


# -------------------------------------------
# 获取负载信息
# -------------------------------------------
def getLoad(host, loid):
    """系统负载"""
    load_oids = '1.3.6.1.4.1.2021.10.1.3.' + str(loid)
    #return snmpWalk(host, load_oids)[0].split(':')[3]
    return snmpWalk(host, load_oids)


def getLoads(host):
    load1 = getLoad(host, 1)
    load10 = getLoad(host, 2)
    load15 = getLoad(host, 3)
    return load1, load10, load15


# ----------------------------------
# 获取网卡流量
# ----------------------------------
def getNetworkDevices(host):
    """获取网络设备信息"""
    device_mib = snmpWalk(host, 'RFC1213-MIB::ifDescr')
    device_list = []
    for item in device_mib:
        device_list.append(item.split(':')[3].strip())
    return device_list


def getNetworkData(host, oid):
    """获取网络流量"""
    data_mib = snmpWalk(host, oid)
    data = []
    for item in data_mib:
        byte = float(item.split(':')[3].strip())
        data.append(str(round(byte/1024, 2)) + 'KB')
    return data


def getNetworkInfo(host):
    device_list = getNetworkDevices(host)
    # 流入流量
    inside = getNetworkData(host, 'IF-MIB::ifInOctets')
    # 流出流量
    outside = getNetworkData(host, 'IF-MIB::ifOutOctets')
    return device_list, inside, outside

# -------------------------------------
# 内存使用率
# -------------------------------------
def getSwapTotal(host):
    swap_total = snmpWalk(host, 'UCD-SNMP-MIB::memTotalSwap.0')[0].split('')[3]
    return swap_total


def getSwapUsed(host):
    swap_avail = snmpWalk(host, 'UCD-SNMP-MIB::memAvailSwap.0')[0].split('')[3]
    swap_total = getSwapTotal(host)
    swap_used = str(round(((float(swap_total) - float(swap_avail))/float(swap_total))*100, 2))
    return swap_used


def getMemTotal(host):
    #mem_total = snmpWalk(host, 'UCD-SNMP-MIB::memTotalReal.0')[0].split('')[3]
    mem_total = snmpWalk(host, 'UCD-SNMP-MIB::memTotalReal.0')
    return mem_total


def getMemUsed(host):
    mem_total = getMemTotal(host)
    mem_avail = snmpWalk(host, 'UCD-SNMP-MIB::memAvailReal.0')
    print(mem_total)
    print(mem_avail)
    mem_used = str(round(((float(mem_total) - float(mem_avail)) / float(mem_total))*100, 2)) + ''
    return mem_used


def getMemInfo(host):
    mem_used = getMemUsed(host)
    swap_used = getSwapUsed(host)
    return mem_used, swap_used

# --------------------------------------------------

def main():
    for host in hosts:
        print('='*10 + host + '=')
        start = time.time()
        print("系统信息")
        system = getSystem(host)
        print(system)

        print("系统负载")
        load1, load10, load15 = getLoads(host)
        print('load(5min):%s, load(10min):%s, laod(15min):%s' %(load1, load10, load15))

        print("网卡流量")
        device_list, inside, outside = getNetworkInfo(host)
        for i, item in enumerate(device_list):
            print('%s: RX: %-15s TX: %s' % (device_list[i], inside[i], outside[i]))

        mem_used, swap_used = getMemInfo(host)
        print("内存使用率")
        print("Mem_Used = %-15s Swap_Used = %-15s" % (mem_used, swap_used))

        end = time.time()
        print('run time:', round(end - start, 2), 's')


if __name__ == '__main__':
    main()