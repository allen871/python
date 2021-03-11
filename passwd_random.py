#!/usr/bin/env python
#coding: utf-8

#生成随机密码

import sys
import random
import string

upasswd="".join(random.sample('123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ!@#$%',9))
print upasswd
