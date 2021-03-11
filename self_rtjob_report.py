#!/usr/bin/python
#coding:utf-8
#自营报表导出，生成execl文件，每日执行

import MySQLdb
import xlwt
import sys
import datetime

date=datetime.date.today() - datetime.timedelta(days=4)
#date='2020-04-08'
filename_date=date.strftime("%Y_%m_%d")
#filename_date='2020_04_08'

db=MySQLdb.connect(host="db-host",user="db-name", passwd="db-pass", db="db-host", port=3306, charset="utf8")
cursor = db.cursor()

table_name={'1000085202':'雷士照明京东自营官方旗舰店','1000148205':'雷士（NVC）浴霸京东自营旗舰店','1000098246':'长虹空调京东自营旗舰店','1000001134':'长虹京东自营旗舰店','1000002368':'Letv超级电视京东自营旗舰店','1000000937':'美菱冰箱洗衣机京东自营旗舰店'}

def sql_query(sql):
    cursor.execute(sql)
    results=cursor.fetchall()
    return results

def payment_sum(shop_id,trade_id):
    "根据trade_id计算付款金额求和"
    d = {}
    sql_trade_id="SELECT trade_id,payment FROM `pes_order`where shop_id =%s and direct_trade_id in(%s) or trade_id in(%s)" % (shop_id,trade_id,trade_id)
    lst=sql_query(sql_trade_id)
    if not lst:
        return
    for item in lst:
        if item[0] in d:
          d[item[0]] = d[item[0]] + item[1]
        else:
            d[item[0]] = item[1]
    return d[item[0]]

def report_data(key,rs):    
    "获取重新计算之后的数据"
    data=[]
    for r in rs:
        if r[8] !=None and r[7]==0:
            r=list(r)
            if payment_sum(key,r[5]) != None:
                r[7]=payment_sum(key, r[5])
            data.append(r)
        else:
            r=list(r)
            data.append(r)
    return data

def set_style(style,col):
    if col in (2,4,6,8):
        style.num_format_str ='yyyy:mm:dd hh:mm:ss'
    if col == 5:
        style.num_format_str ='0'
    if col == 0:
        style.num_format_str ='0'
    if col == 7:
        style.num_format_str ='0.000'
    return style
def execl_write(table_name):
    "将重新计算之后的数据写入excel"
    wb = xlwt.Workbook(encoding ='utf-8')
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = u'宋体'
    font.height = 20 * 12
    style.font=font
    for key,value in table_name.items():
        sql_data="SELECT shop_id as '店铺id', buyer_nick as '买家昵称',created as '创建时间', cs_nick as '绩效客服', modified as '执行时间', order_id as '订单id' , \
        order_created '订单创建时间', payment as '订单金额', pay_time as '付款时间', CASE WHEN STATUS =0 THEN '分配' WHEN STATUS = 1 THEN '已执行' \
        WHEN STATUS = 2 THEN '已忽略' WHEN STATUS = 3 THEN '已失效' ELSE '默认值' END AS '任务状态', CASE WHEN result =0 THEN '进行中' WHEN result = 1 THEN '成功' \
        WHEN result = 2 THEN '失败' WHEN result = 3 THEN '失效' END AS '任务结果', CASE WHEN task_type =1 THEN '咨询未下单' WHEN task_type = 2 THEN '咨询下单未付款' \
        WHEN task_type = 3 THEN '静默下单未付款' WHEN task_type = 3 THEN '失效' END AS '任务分类', CASE \
        WHEN closure_type =1 THEN '否' WHEN closure_type = 2 THEN '是' END AS '是否是截流'\
        FROM `pes_cs_conversion` WHERE shop_id=%s and created BETWEEN '%s 00:00:00' and '%s 23:59:59'" % (key,date,date)
        cursor.execute(sql_data)
        rs=cursor.fetchall()
        fields=cursor.description
        data=report_data(key,rs)

        #写入列名
        sh = wb.add_sheet(value)
        #设置单元格宽度
        sh.col(0).width= 256 * 12
        sh.col(1).width= 256 * 20
        sh.col(2).width= 256 * 22
        sh.col(3).width= 256 * 18
        sh.col(4).width= 256 * 22
        sh.col(5).width= 256 * 14
        sh.col(6).width= 256 * 22
        sh.col(7).width= 256 * 10
        sh.col(8).width= 256 * 22
        sh.col(9).width= 256 * 9
        sh.col(10).width= 256 * 9
        sh.col(11).width= 256 * 17
        sh.col(12).width= 256 * 11
        for field in range(0, len(fields)):
            sh.write(0, field, fields[field][0],style)
        #开始写入excel数据
        start_row_num=1
        for data_list in data:
            start_col_num=0
            for i in data_list:
                sh.write(start_row_num,start_col_num,i,set_style(style,start_col_num))
                start_col_num+=1
            start_row_num+=1
        print "%s 写入完成" % value
    
    db.close()
    wb.save('催付明细报表_'+filename_date+'.xls')

#生成execl    
execl_write(table_name)
