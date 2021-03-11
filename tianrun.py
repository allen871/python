#!/usr/bin/env python
#coding: utf-8
# 天润满意度接口调用

import requests
import hashlib
import time
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


startdate=datetime.datetime.now() - datetime.timedelta(minutes=5)
startdate=startdate.strftime("%Y-%m-%d %H:%M:%S")
enddate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def getData():

    url="http://api.clink.cn/interface/entrance/OpenInterfaceEntrance"
    payload={'enterpriseId':'3003579',
  	     'interfaceType':'investigationList',
	     'userName':'system',
	     'pwd':'bfb80b30cc82b9fa412ce55a376c01be',
	     'startDate':startdate,
	     'endDate':enddate
	   }
    r=requests.post(url, data=payload)
    return r.text

def sendData():

    ck_sign='D9FACF0B18BE36BE115FD4ACE7505D0A'
    data=getData()
#    print type(data)
#    sys.exit()
    url="http://zx.admin.51youjuke.com/satisfaction/satisfactions_save_api"
    payload={'ck_sign':ck_sign,
	     'data':data
	    } 
#    payload = json.dumps(payload)
#    print payload
    r=requests.post(url, data=payload)
    print '%s----%s' % (startdate,enddate)
#    print r.text
    a = r.json()
    print json.dumps(a, ensure_ascii=False)

if __name__=="__main__":        
    sendData()
