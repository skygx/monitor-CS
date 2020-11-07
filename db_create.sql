create table collectDatas (id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,cpu_usage REAL,cpu_load1 REAL,cpu_load5 REAL,cpu_load15 REAL,mem_total REAL,
mem_free REAL,mem_usage REAL,swap_total REAL,swap_free REAL,swap_percent REAL,recv INTEGER,	send INTEGER,pkg_recv INTEGER,pkg_snd INTEGER);

-- 网络，磁盘，磁盘IO为字符串
create table Datas (id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,cpu_usage REAL,cpu_load1 REAL,cpu_load5 REAL,cpu_load15 REAL,mem_total REAL,
mem_free REAL,mem_usage REAL,swap_total REAL,swap_free REAL,swap_percent REAL,net TEXT,disk TEXT,diskio TEXT);

-- 分表 CPU
create table cpuMsg(id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,cpu_usage REAL,cpu_load1 REAL,cpu_load5 REAL,cpu_load15 REAL);

-- 内存
create table memMsg(id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,mem_total REAL,mem_free REAL,mem_usage REAL);

-- 交换分区
create table swapMsg(id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,swap_total REAL,swap_free REAL,swap_percent REAL);

-- 网络IO
create table netMsg(id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,net_name TEXT,recv INTEGER,send INTEGER,pkg_recv INTEGER,pkg_snd INTEGER,errin INTEGER ,errout INTEGER,dropin INTEGER,dropout INTEGER);

-- 磁盘容量
create table diskMsg(id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,disk_mount TEXT,disk_name TEXT,total_disk_size REAL,used_disk_size REAL,free_disk_size REAL,percent_disk REAL);

-- 磁盘IO
create table diskioMsg(id INTEGER PRIMARY KEY AUTOINCREMENT,ip TEXT NOT NULL,tm INTEGER NOT NULL,host TEXT NOT NULL,dname TEXT,read_count INTEGER,write_count INTEGER,read_bytes REAL,write_bytes REAL,read_time INTEGER,write_time INTEGER);