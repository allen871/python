#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import smtplib
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import Encoders
import os

mail_host = 'mail-server' #smtp服务器地址
mail_user = 'aaa@test.com'        #发件人邮箱
mail_pwd = 'password'                     #邮箱密码
# mail_to = "allen@360iii.com"                                       #多个用户使用英文标点;分割
# mail_cc = ''                                                       #抄送 如果没有设为空
# mail_bcc = ''                                                      #密送 如果没有设为空


def send_email(subject,content,mail_to,mail_cc=None,mail_bcc=None,attach_filenames=[]):
    #表头信息
    msg = MIMEMultipart('related')
    msgText = MIMEText(content,_charset='utf-8')
    msg.attach(msgText)

    msg['From'] = mail_user
    msg['Subject'] = subject
    msg['To'] = mail_to

    if attach_filenames:
        for file_name in attach_filenames:
            # file_name = "music.txt"
            att = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')#添加附件
            att["Content-Type"] = 'application/octet-stream'
            #att["Content-Disposition"] = 'attachment; filename="%s"' % file_name.encode('gbk')
            att["Content-Disposition"] = 'attachment; filename="%s"' % file_name
            msg.attach(att)

    if mail_cc:msg['Cc'] = mail_cc
    if mail_bcc:msg['Bcc'] = mail_bcc
    try:
        s = smtplib.SMTP()
        s.connect(mail_host,port=25)
        #login
        s.login(mail_user,mail_pwd)

        #send mail
        toaddrs = mail_to.split(';')
        if mail_cc:toaddrs=toaddrs+mail_cc.split(';')
        if mail_bcc:toaddrs=toaddrs+mail_bcc.split(';')

        s.sendmail(mail_user,toaddrs,msg.as_string())
        s.close()
        print 'send email to %s success' % toaddrs
    except Exception ,e:
        print e



