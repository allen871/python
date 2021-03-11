#!/usr/bin/python
# coding:utf-8
# __author__ = ''

#远程连接执行命令

import pexpect
import sys

child = pexpect.spawn('ssh root@192.168.1.7')

#fout = file('mylog.txt', 'w')
#child.logfile = fout

i = child.expect(['password:', 'continue connecting(yes/no)?'], timeout=30)

if i == 0:
    child.sendline("ssh密码")

if i == 1:
    child.sendline('yes')
    child.expect('[p,P]assword: ') #Password/password
    child.sendline('ssh密码')

child.expect('#')
child.sendline('ls')
child.expect('#')
print 'before: '+child.before
print 'after: '+child.after
