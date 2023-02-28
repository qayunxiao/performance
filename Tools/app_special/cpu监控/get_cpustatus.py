# -*- coding: utf-8 -*-
# @Time    : 2022/12/26 9:13
# @Author  : alvin
# @File    : get_cpustatus.py
# @Software: PyCharm
import csv
import os
import time


class Controller(object):
    def __init__(self,count):
        self.counter = count
        self.alldata= [("timestamp","cpustatus","user","kernel")]

    def runone(self):
        print("run")
        #注意在windows电脑上，用findstr ；在苹果本上用grep
        # +0% 2679/com.lemon.lemonban: 0% user + 0% kernel
        res = os.popen(" adb shell dumpsys cpuinfo | findstr system_server")
        cpuvalue ="0"
        user ="0"
        kernel ="0"
        for line in res.readlines():
            cpuvalue = line.split("%")[0]
            user =line.split("%")[1].split(": ")[1]
            kernel = line.split("%")[2].split("+")[1]
            print("line",line)
        currenttime = self.getCurrentTime()
        print(currenttime,cpuvalue,user,kernel)
        self.alldata.append((currenttime,cpuvalue,user,kernel))

    #多次执行测试过程
    def run_times(self):
        while self.counter >0:
            self.runone()
            self.counter = self.counter - 1
            time.sleep(10)

    def savedata_tocsv(self):
        print("写文件",self.alldata)
        file_name = "cpu.csv"
        file_patn = os.path.dirname(os.path.abspath(__file__))
        file_name_ful=os.path.join(file_patn,file_name)
        # csv 模块中的 writer 类可用于读写序列化的数据
        with open(file_name_ful,'w',newline='') as f:
            writer = csv.writer(f)
            # 注意传入数据的格式为列表元组格式
            writer.writerows(self.alldata)

        #获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

if __name__ == '__main__':
    controller = Controller(5)
    # controller.runone()
    controller.run_times()
    controller.savedata_tocsv()
