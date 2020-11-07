#/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    @File    :   data-report-v1.py
    @Contact :   guoxin@126.com
    @License :   (C)Copyright 2018-2019, xguo

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/10/30  13:15   xguo      1.0         None

'''
import sqlite3

def get_host():
    conn = sqlite3.connect("data_collect.db")
    cs = conn.cursor()
    sql = "select distinct(host) from collectDatas"
    cs.execute(sql)
    result = cs.fetchall()
    cs.close()
    conn.close()

    # print result
    return result

def get_data():
    hosts = get_host()
    conn = sqlite3.connect("data_collect.db")
    cs = conn.cursor()
    data = {}
    for h in hosts:
        h = str(h[0]).decode('utf-8').strip("'")
        # print h
        sql = "SELECT ip,host,cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free, mem_usage, swap_total, swap_free, swap_percent, recv, send, pkg_recv, pkg_snd FROM collectDatas  where host = \"{}\" order by tm desc limit 1".format(h)
        cs.execute(sql)
        data[h] = cs.fetchall()
    cs.close()
    conn.close()
    print data
    return data

def print_data():
    datas = get_data()
    header = "ip,host,cpu_usage, cpu_load1, cpu_load5, cpu_load15, mem_total, mem_free, mem_usage, swap_total, swap_free, swap_percent, recv, send, pkg_recv, pkg_snd\n"
    # print datas
    result = []
    with open('./report.csv','w') as f:
        f.write(header)
        for value in datas.values():
            data = ','.join(str(v).decode('utf-8').strip("'") for v in value[0])
            print data
            result.append(data+'\n')
        f.writelines(result)

def main():
    # get_data()
    print_data()

if __name__ == "__main__":
    main()