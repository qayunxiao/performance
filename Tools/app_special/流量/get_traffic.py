# -*- coding: utf-8 -*-
# @Time    : 2022/12/26 17:45
# @Author  : alvin
# @File    : get_traffic.py
# @Software: PyCharm
import csv
import os
import time

#/usr/bin/python
#encoding:utf-8
import csv
import os
import time

#控制类
class Controller(object):
    def __init__(self, count):
        #定义测试的次数
        self.alldata = []
        self.counter = count
        #定义收集数据的数组
        self.fieldnames = ["timestamp", "traffic"]
        self.Dictfile_name = "trafficstatus.csv"
        self.receive=0
        self.transmit=0
        self.receive2=0
        self.transmit2=0






#单次测试过程
    def testprocess(self):
        #执行获取进程的命令
        result = os.popen("adb shell ps  | findstr com.lemon.lemonban")
        #获取进程ID
        pid = result.readlines()[0].split(" ")[5]
        print("pid",pid)

        #获取进程ID使用的流量
        traffic = os.popen("adb shell cat /proc/"+pid+"/net/dev")
        for line in traffic:
            if "eth0" in line:
                print("line eth0 1",line)
                #将所有空行换成#
                line = "#".join(line.split())
                print("line eth0 2",line)
            #按#号拆分,获取收到和发出的流量
                self.receive = line.split("#")[1]
                print("receive",self.receive)
                self.transmit = line.split("#")[9]
                print("transmit",self.transmit)
            elif "eth1" in line:
                print("line eth1 ",line)
                # 将所有空行换成#
                line =  "#".join(line.split())
                # 按#号拆分,获取收到和发出的流量
                self.receive2 = line.split("#")[1]
                self.transmit2 = line.split("#")[9]

        #计算所有流量的之和
        alltraffic = int(self.receive) +  int(self.transmit) +  int(self.receive2) +  int(self.transmit2)
        #按KB计算流量值
        alltraffic = alltraffic/1024
        #获取当前时间
        currenttime = self.getCurrentTime()
        #将获取到的数据存到数组中
        self.alldata.append({'timestamp':currenttime,"traffic":alltraffic})

    #多次测试过程控制
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1
            #每5秒钟采集一次数据
            time.sleep(5)

    #获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据的存储
    def save_data_csv_dict(self):
        print("self.alldata",self.alldata)
        with open(self.Dictfile_name,"w",newline='') as csv_f:
            #表字段名
            writer=csv.DictWriter(csv_f,fieldnames=self.fieldnames)
            writer.writeheader()#写表头
            # 多行写入
            writer.writerows(self.alldata)
            # 单行写入
            # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})


if __name__ == "__main__":
    controller = Controller(5)
    controller.run()
    controller.save_data_csv_dict()