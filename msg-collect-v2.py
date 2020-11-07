#/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    @File    :   msg-collect-v1.py
    @Contact :   guoxin@126.com
    @License :   (C)Copyright 2018-2019, xguo

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/10/29  11:09   xguo      1.0         None

'''

import psutil
from socket import *
import time
import os
import logging
import json
import pprint

address='192.168.136.110'   #测试服务器的ip地址
# address='10.111.251.66'   #服务器的ip地址

port=12345           #服务器的端口号
buffsize=2048        #接收数据的缓存大小
s=socket(AF_INET, SOCK_STREAM)
s.connect((address,port))
t = 2

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("collect.log")
fh.setLevel(logging.INFO)
# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
#将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)

unit = {'G': 1024*1024*1024, 'M': 1024*1024, 'K':1024}

def get_cpu_info():
    logger.info("cpu info message:")
    cpu1 = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent()
    cpu_load1,cpu_load5,cpu_load15 = os.getloadavg()

    info = "Cpu Load:{},Cpu Usage:{}%".format(cpu_load1,cpu_usage)
    logger.info(info)
    return cpu_usage,cpu_load1,cpu_load5,cpu_load15


def get_mem_info():
    logger.info("mem info message:")
    mem = psutil.virtual_memory()
    mem1 = str(mem.total / unit['M'] )
    mem2 = str(mem.free / unit['M'] )
    mem_usage = str(mem.percent)
    cache = str(mem.cached / unit['M'])

    info = "Mem Total:{} MB,Mem Free:{} MB,Mem Percent:{}%,Cache:{} MB".format(mem1[0:4], mem2[0:4],mem_usage,cache)
    logger.info(info)
    return mem1[0:4],mem2[0:4],mem_usage

def get_swap_info():
    logger.info("swap info message:")
    swap = psutil.swap_memory()
    total = str(swap.total /unit['M'])
    free = str(swap.free / unit['M'])
    percent = swap.percent

    info = "Swap Total:{} MB,Swap Free:{} MB,Swap Percent:{}%".format(total,free,percent)
    logger.info(info)
    return total,free,percent

def sys_pid():
    logger.info("process pids message:")
    pids = psutil.pids()
    logger.info(pids)

def get_net_info():
    logger.info("net info message:")
    net_io = psutil.net_io_counters(pernic=True)
    content = ""
    data = {}
    for net_name,net_info in net_io.items():
        recv = net_info.bytes_recv
        send = net_info.bytes_sent
        pkg_recv = net_info.packets_recv
        pkg_snd = net_info.packets_sent
        errin = net_info.errin
        errout = net_info.errout
        dropin = net_info.dropin
        dropout = net_info.dropout

        info = "{}: recv:{} MB send:{} MB pkg_recv:{} pkg_snd:{};".format(net_name,recv/unit['M'] ,send/unit['M'],pkg_recv,pkg_snd)
        #保存数据
        data[net_name] = [recv,send,pkg_recv,pkg_snd,errin,errout,dropin,dropout]
        # print (info)
        #保存为字符串形式
        content = content + info

    # pprint.pprint(data)
    result = json.dumps(data)
    logger.info(content)
    return content,result

def get_host_info():
    logger.info("host info message:")
    import socket
    host = socket.gethostname()
    info = "Host:{}".format(host)
    logger.info(info)
    return host

def get_iops_info():
    logger.info("disk io info message:")
    disk_io = psutil.disk_io_counters(perdisk=True)
    content = ""
    data = {}
    for dname,dinfo in disk_io.items():
        read_count = dinfo.read_count
        write_count = dinfo.write_count
        read_bytes = dinfo.read_bytes
        write_bytes = dinfo.write_bytes
        read_time = dinfo.read_time
        write_time = dinfo.write_time

        info = "{}: read:{} write:{} read_bytes:{} MB write_bytes:{} MB;".format(dname,read_count,write_count,read_bytes/unit['M'],write_bytes/unit['M'])
        # 保存数据
        data[dname] = [read_count,write_count,read_bytes,write_bytes,read_time,write_time]
        # 保存为字符串形式
        content = content + info

    # pprint.pprint(data)
    logger.info(content)
    result = json.dumps(data)
    return content,result

def get_disk_info():
    logger.info("disk info message")
    content = ""
    data = {}
    # 循环磁盘分区
    for disk in psutil.disk_partitions():
        # 读写方式 光盘 or 有效磁盘类型
        if 'cdrom' in disk.opts or disk.fstype == '':
            continue
        disk_name_arr = disk.device.split(':')
        disk_mount = disk.mountpoint
        disk_name = disk_name_arr[0]
        disk_info = psutil.disk_usage(disk_mount)
        # 磁盘剩余空间，单位G
        free_disk_size = disk_info.free// unit['G']
        # 磁盘全部空间，单位G
        total_disk_size = disk_info.total// unit['G']
        # 磁盘已用空间，单位G
        used_disk_size = disk_info.used// unit['G']
        # 磁盘使用率
        percent_disk = disk_info.percent
        # 当前磁盘使用率和剩余空间G信息
        info = "Disk Mount:{} Disk Percent:{} % Disk Free:{} GB;".format(disk_mount, str(percent_disk), free_disk_size)
        # print(info)
        # 拼接多个磁盘的信息
        content = content + info
        data[disk_mount] = [disk_name,total_disk_size,used_disk_size,free_disk_size,percent_disk]

    # pprint.pprint(data)
    logger.info(content)
    result = json.dumps(data)
    return content,result


def writePid():
    logger.info("save agent pid")
    pid = str(os.getpid())
    f = open('collect.pid', 'w')
    logger.info(pid)
    f.write(pid)
    f.close()

def main():
    writePid()
    while True:
        tm = time.strftime('%Y-%m-%d %X')
        #获取CPU数据
        cpu_usage,cpu_load1,cpu_load5,cpu_load15 = get_cpu_info()
        #获取内存数据
        mem_total,mem_free,mem_usage = get_mem_info()
        #获取交换分区数据
        swap_total,swap_free,swap_percent = get_swap_info()
        #获取主机名
        host = get_host_info()
        #获取网络数据
        netstr,netdata = get_net_info()
        #获取磁盘使用空间
        diskstr,diskdata = get_disk_info()
        #获取磁盘IO性能
        diskiostr,diskiodata = get_iops_info()
        print netdata
        print diskdata
        print diskiodata
        data = [tm,host,cpu_usage,cpu_load1,cpu_load5,cpu_load15,mem_total,mem_free,mem_usage,swap_total,swap_free,swap_percent,netstr,diskstr,diskiostr,netdata,diskdata,diskiodata]
        print len(data)
        data = map(str,data)
        senddata = '|'.join(data)
        if len(senddata) == 0 :
            break
        s.send(senddata.encode())
        recvdata = s.recv(buffsize).decode('utf-8')
        print(recvdata)
        logger.info("{}".format(senddata))
        time.sleep(t)
    s.close()


if __name__ == "__main__":
    main()
