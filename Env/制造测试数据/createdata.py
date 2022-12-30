# -*- coding: utf-8 -*-
# @Time    : 2022/12/30 15:18
# @Author  : alvin
# @File    : createdata.py
# @Software: PyCharm
import pymysql
import time
#创建链接mysql
conn=pymysql.Connect(host='127.0.0.1',port=3306,user='qa',password='qatest'
                    ,database='jmeter' )
# 创建游标 2021-08-08 17:43:30
cursor = conn.cursor()
c_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
print(c_time,type(c_time))
sql1=" INSERT into `book` (`id`,`book_name`,`author_name`,`last_index_update_time`,`create_time`)  " \
     "VALUES ('{}','{}','{}','{}','{}');"
id_start=1000
book_name='反派生涯'
author_name='作者：桃符'
for i in range(10000):
    id_s=id_start+i
    print("当前第",i,"条数据，内容->",sql1.format(int(id_s),book_name+str(i),author_name+str(i),c_time,c_time))
    cursor.execute(sql1.format(int(id_s),book_name+str(i),author_name+str(i),c_time,c_time))
    # cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()