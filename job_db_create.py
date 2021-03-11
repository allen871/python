#!/usr/bin/python
#coding:utf8

#云鼎每日Job，每月建表

import MySQLdb
import sys
import datetime
from dateutil.relativedelta import relativedelta

datetime_now = datetime.datetime.now()
datetime_one_month_later = datetime_now + relativedelta(months=1)

#获取下一个月日期
tableDateNext=datetime_one_month_later.strftime('%Y_%m')
#获取当前月日期
tableDate=datetime.datetime.now().strftime('%Y_%m')

db_host_list=['db-host01','db-host02','db-host03','db-host04']

db_list=['db-name01','db-name01','db-name01']

for db_host in db_host_list:
    for i in db_list:
        db=MySQLdb.connect(db_host, "username", "password", i, charset='utf8')
        cursor=db.cursor()
        cursor.execute("show tables")
        for line in cursor.fetchall():
            line="%s" % line
            if line.find(tableDate) >-1:
                tableName=line.rstrip(tableDate)
                sql="create table if not exists %s_%s like %s" % (tableName,tableDateNext,line)
                cursor.execute(sql)
                print sql

        db.close()


s