# -*- coding: utf-8 -*-
# @Time    : 2022/12/26 9:13
# @Author  : alvin
# @File    : get_menmstatus.py
# @Software: PyCharm
import csv
import os
import time


class Controller(object):
    def __init__(self,count):
        self.pid = 0
        self.counter = count
        self.alldata= []
        self.fieldnames = ['time',"Java Heap","Dalvik Heap"]
        self.datalist =[]
        self.Dictfile_name = "menmstatus.csv"


    def get_pid(self):
        res = os.popen("adb shell ps  | findstr com.lemon.lemonban")
        #u0_a44    2235  1079  1377168 195588          0 c7f28c10 S com.lemon.lemonban
        for line in res.readlines():
            self.pid=line.split("  ")[2]
        if 0 != self.pid:
            return self.pid
        else:
            exit(1)

    def get_findstr(self,line1,str_1):
        if line1.find(str_1) > -1:
            # print("line",line)
            data=line1[(line1.find(str_1)+len(str_1)):].lstrip().rstrip("\n")
            print("data",data)
            return  data
    def run_times(self):
        while self.counter > 0:
            self.runone()
            time.sleep(10)
            self.counter -=1

    def runone(self):
        print("run",self.pid)
        cmd ="adb shell dumpsys meminfo {}".format(self.pid)
        res = os.popen(cmd)
        for line in res.readlines():
            str_1=" Native Heap:"
            if line.find(str_1) > -1:
                nativeheap=line[(line.find(str_1)+len(str_1)):].lstrip().rstrip("\n")
            str_2="          Java Heap:"
            if line.find(str_2) > -1:
                javaheap=line[(line.find(str_2)+len(str_2)):].lstrip().rstrip("\n")
        currenttime = self.getCurrentTime()
        #{'first_name': 'Baked', 'last_name': 'Beans'}
        # self.fieldnames = ['time',"Java Heap","Dalvik Heap"]
        self.alldata.append({'time':currenttime,"Java Heap":javaheap,"Dalvik Heap":nativeheap})

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

    # 获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

if __name__ == '__main__':
    controller = Controller(3)
    controller.get_pid()
    controller.run_times()
    # controller.runone()
    controller.save_data_csv_dict()
