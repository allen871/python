#!/usr/bin/python
# coding:utf-8

'''tcp端口连接测试'''

import socket
import re
import sys

def check_server(address, port):
    s = socket.socket()
    print "尝试连接%s的%s端口" % (address, port)
    try:
        s.connect((address, port))
        print "连接成功%s的%s端口" % (address, port)
        return True
    except socket.error, e:
        print "不能连接到%s的%s端口" % (address, port)
        return False

if __name__=='__main__':
    check_server('192.168.5.146', int('3301'))