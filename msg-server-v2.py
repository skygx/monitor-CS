#/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    @File    :   msg-server-v1.py
    @Contact :   guoxin@126.com
    @License :   (C)Copyright 2018-2019, xguo

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/10/29  11:35   xguo      1.0         None

'''
from socket import *
import threading
import sqlite3
import logging
import json

address='0.0.0.0'     #监听哪些网络  127.0.0.1是监听本机 0.0.0.0是监听整个网络
port=12345             #监听自己的哪个端口
buffsize=2048         #接收从客户端发来的数据的缓存区大小
s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
s.listen(1024)     #最大连接数

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("server.log")
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

def conv_netdata(ip,tm,host,conn,netdata):
    logger.info("convert {} net data start".format(host))
    c = conn.cursor()
    for name,data in netdata.items():
        # print "{},{},{},{},{},{},{},{},{}".format(name,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
        sql = '''
            INSERT INTO netMsg('ip','tm', 'host','net_name','recv','send','pkg_recv','pkg_snd','errin','errout','dropin','dropout')
            values(\"{}\",\"{}\",\"{}\",\"{}\",{},{},{},{},{},{},{},{})
            '''.format(ip, tm, host,name,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
        c.execute(sql)
        conn.commit()
    logger.info("convert {} net data stop".format(host))

def conv_diskdata(ip,tm,host,conn,diskdata):
    logger.info("convert {} disk data start".format(host))
    c = conn.cursor()
    for name,data in diskdata.items():
        print "{},{},{},{},{},{}".format(name,data[0],data[1],data[2],data[3],data[4])
        sql = '''
            INSERT INTO diskMsg('ip','tm', 'host','disk_mount','disk_name','total_disk_size','used_disk_size','free_disk_size','percent_disk')
            values(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",{},{},{},{})
            '''.format(ip, tm, host,name,data[0],data[1],data[2],data[3],data[4])
        c.execute(sql)
        conn.commit()
    logger.info("convert {} disk data stop".format(host))

def conv_diskiodata(ip,tm,host,conn,diskiodata):
    logger.info("convert {} disk io data start".format(host))
    c = conn.cursor()
    for name,data in diskiodata.items():
        print "{},{},{},{},{},{},{}".format(name,data[0],data[1],data[2],data[3],data[4],data[5])
        sql = '''
            INSERT INTO diskioMsg('ip','tm', 'host','dname','read_count','write_count','read_bytes','write_bytes','read_time','write_time')
            values(\"{}\",\"{}\",\"{}\",\"{}\",{},{},{},{},{},{})
            '''.format(ip, tm, host,name,data[0],data[1],data[2],data[3],data[4],data[5])
        c.execute(sql)
        conn.commit()
    logger.info("convert {} disk io data stop".format(host))

def tcplink(sock,addr):
    logger.info("start {}".format(addr))
    while True:
        recvdata=sock.recv(buffsize).decode('utf-8')
        conn = sqlite3.connect('data_collect.db')
        c = conn.cursor()
        data=recvdata.split('|')
        ip,port = addr
        logger.info("receive data len: {}".format(len(data)))
        tm, host, cpu_usage, cpu_load1, cpu_load5, cpu_load15, \
        mem_total, mem_free, mem_usage, \
        swap_total, swap_free, swap_percent, \
        netstr,diskstr,diskiostr,\
        netdata,diskdata,diskiodata= data

        net = json.loads(netdata)
        disk = json.loads(diskdata)
        diskio = json.loads(diskiodata)

        logger.info("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(ip,port,tm, host, cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free, mem_usage, swap_total, swap_free, swap_percent,netstr,diskstr,diskiostr))
        sql = '''
                    INSERT INTO Datas('ip','tm', 'host', 'cpu_usage', 'cpu_load1', 'cpu_load5', 'cpu_load15', 'mem_total', 'mem_free', 'mem_usage', 'swap_total', 'swap_free', 'swap_percent', 'net', 'disk', 'diskio')
                    values(\"{}\",\"{}\",\"{}\",{},{},{},{},{},{},{},{},{},{},\"{}\",\"{}\",\"{}\")
                    '''.format(ip, tm, host, cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free,mem_usage, swap_total, swap_free, swap_percent, netstr, diskstr, diskiostr)

        c.execute(sql)

        conn.commit()

        conv_netdata(ip, tm, host, conn, net)

        conv_diskdata(ip, tm, host, conn, disk)

        conv_diskiodata(ip, tm, host, conn, diskio)

        sock.send(recvdata.encode())

    conn.close()
    sock.close()
    logger.info("stop {}".format(addr))

def main():
    logger.info("data collect server start!")
    while True:
        clientsock, clientaddress = s.accept()
        logger.info('connect from: {}'.format(clientaddress))
        # 传输数据都利用clientsock，和s无关
        t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))  # t为新创建的线程
        t.start()
    s.close()
    logger.info("data collect server stop!")

if __name__ == "__main__":
    main()