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

address='0.0.0.0'     #监听哪些网络  127.0.0.1是监听本机 0.0.0.0是监听整个网络
port=12345             #监听自己的哪个端口
buffsize=1024          #接收从客户端发来的数据的缓存区大小
s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
s.listen(1024)     #最大连接数



def tcplink(sock,addr):
    while True:
        recvdata=sock.recv(buffsize).decode('utf-8')
        conn = sqlite3.connect('data_collect.db')
        c = conn.cursor()
        senddata=recvdata
        ip,port = addr
        tm, host, cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free, mem_usage, swap_total, swap_free, swap_percent, recv, send, pkg_recv, pkg_snd = recvdata.split(',')
        print (ip,port,tm, host, cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free, mem_usage, swap_total, swap_free, swap_percent,recv, send, pkg_recv, pkg_snd)
        sql = '''
            INSERT INTO collectDatas('ip','tm', 'host', 'cpu_usage', 'cpu_load1', 'cpu_load5', 'cpu_load15', 'mem_total', 'mem_free', 'mem_usage', 'swap_total', 'swap_free', 'swap_percent', 'recv', 'send', 'pkg_recv', 'pkg_snd') 
            values(\"{}\",\"{}\",\"{}\",{},{},{},{},{},{},{},{},{},{},{},{},{},{})
            '''.format(ip,tm, host, cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free, mem_usage, swap_total, swap_free, swap_percent, recv, send, pkg_recv, pkg_snd)

        c.execute(sql)
        # print ("{}:{}".format(addr,senddata))
        conn.commit()
        sock.send(senddata.encode())
    conn.close()
    sock.close()

def main():
    while True:
        clientsock, clientaddress = s.accept()
        print('connect from:', clientaddress)
        # 传输数据都利用clientsock，和s无关
        t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))  # t为新创建的线程
        t.start()
    s.close()

if __name__ == "__main__":
    main()