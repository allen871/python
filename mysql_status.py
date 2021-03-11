#!/usr/bin/env python
# coding:utf-8

#判断mysql是否连接正常

import MySQLdb
import datetime
import sys
from send_email import send_email

try:
    mysql_conf = {'host':'db-host','user':'username','passwd':'password','db':'db-name','charset':'utf8'}
    conn = MySQLdb.connect(**mysql_conf)
    cur = conn.cursor()
    sql ='select version()'
    # print sql
    cur.execute(sql)
except Exception as e:
    send_email(u'mysql连接错误',u'mysql无法连接!','email地址')
    sys.exit(1)

result = cur.fetchone()
result="".join(tuple(result))
conn.close()
if result != "5.6.23-log":
    send_email(u'mysql连接错误',u'未知错误!','email地址')
