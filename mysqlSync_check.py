#!/usr/bin/env python
# coding:utf-8

#mysql主从数据一致检测

import MySQLdb
import commands
import time
import os
import send_email

#数据库连接
ip_master='127.0.0.1'
ip_slave='192.168.5.171'
user='monitoruser'
pw='123456'
db="test01"

con=MySQLdb.connect(ip_master,user,pw,db)
cur=con.cursor()
cur.execute("show databases")
databases=cur.fetchall()


data=[]
d1=time.strftime("%Y.%m.%d", time.localtime())

#循环遍历各个数据库中不一致的数据
for database in databases:
	database="".join(database)
	if database == 'mysql' or database == 'information_schema' or database =='performance_schema':
		pass
	else:
		num=commands.getoutput("pt-table-checksum --nocheck-replication-filters --no-check-binlog-format --replicate=%s.checksums  --databases=%s h=%s,u=%s,p=%s,P=3306 | awk '{print $3}' | sed -n '4,$p'" % (database, database,ip_master,user,pw))
		for i in num:
			i=i.strip()
			if i == "1":
				datalog=commands.getoutput("pt-table-sync --replicate=%s.checksums h=%s,u=%s,p=%s h=%s,u=%s,p=%s --print" % (database,ip_master,user,pw,ip_slave,user,pw))
				data.append(datalog)
				break
		

#数据写入日志文件，并发送邮件
data="\n\n\n".join(data)
if os.path.exists("check_log"):
	with open('check_log/checkLog-'+ d1 +'.txt', 'w') as f:
		f.write(data)
	send_email.send_email("mysql主从数据不一致",data,"email地址")
else:
	os.makedirs("check_log")
	with open('check_log/checkLog-'+ d1 +'.txt', 'w') as f:
		f.write(data)
	send_email.send_email("mysql主从数据不一致",data,"email地址")


