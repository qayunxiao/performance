# -*- coding: utf-8 -*-
# @Time    : 2022/12/26 18:10
# @Author  : alvin
# @File    : launchTime.py
# @Software: PyCharm
import csv
import os
import time


class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0


    #启动App
    def LaunchApp(self):
        cmd = 'adb shell am start -W -n com.lemon.lemonban/com.lemon.lemonban.activity.WelcomeActivity'
        self.content=os.popen(cmd)

    #停止App
    def StopApp(self):
        cmd = 'adb shell am force-stop com.lemon.lemonban'
        # cmd = 'adb shell input keyevent 3'
        os.popen(cmd)

    #获取启动时间
    def GetLaunchedTime(self):
        for line in self.content.readlines():
            if "ThisTime" in line:
                self.startTime = line.split(":")[1].rstrip("\n")
                break
        return self.startTime

#控制类
class Controller(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.alldata = []
        self.Dictfile_name="launchTime.csv"
        self.fieldnames =["timestamp","elapsedtime"]

    #单次测试过程
    def testprocess(self):
        self.app.LaunchApp()
        time.sleep(5)
        elpasedtime = self.app.GetLaunchedTime()
        self.app.StopApp()
        time.sleep(3)
        currenttime = self.getCurrentTime()
        self.alldata.append ({"timestamp":currenttime,"elapsedtime":elpasedtime})

    #多次执行测试过程
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1

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

if __name__ == "__main__":
    controller = Controller(10)
    controller.run()
    controller.save_data_csv_dict()