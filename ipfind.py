#!/usr/bin/python
#coding:utf-8


import time
from collections import Counter
import datetime

def ipCount(List):
    ip_list = []
    for i in Counter(List):
        if Counter(List)[i] >=  10:
            ip_list.append(i)
    return ip_list

file='zxgs_log.txt'
delta= datetime.timedelta(days=1)
d1 = 20180419

iplist = []

f = open(file, 'r')
for line in f:
    ip = line.split(" ")[0].strip()
    d = line.split(" ")[3].strip('[')
    d = time.mktime(time.strptime(d, "%d/%b/%Y:%H:%M:%S"))
    d = time.strftime("%Y%m%d",time.localtime(d))
    iplist.append(ip)

    # print "测试 %s" % d1
    if int(d) != int(d1):
        ip_list = ipCount(iplist)
        if ip_list:
            f2 = open("log/%s.log" % d1, "r")
            for line1 in f2:
                ip1 = line1.split(" ")[0]
                if ip1 in ip_list:
                    f3 = open("log1/%s-%s.log" % (d1, ip1), "a")
                    f3.write(line1)
                    f3.close()
            f2.close()

        iplist = []
        d1 = datetime.datetime.strptime("%s" % str(d1), "%Y%m%d")
        d1 = d1 + delta
        d1 = d1.strftime('%Y%m%d')

    # print "测试1 %s" % d1
    if int(d) == int(d1):
        f1 = open("log/%s.log" % d, "a")
        f1.write(line)
        f1.close()

f.close()
