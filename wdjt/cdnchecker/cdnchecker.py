# -*- coding: utf-8 -*-
import threading
import time
import httplib
import hashlib
import urllib2
import myUtil
import os
import json

lock = threading.Lock()
g_finish_flag = 0

BUFFER_DIR = "cdnchecker/buffer/"

def calcMD5(path):
    with open(path, "rb") as file:
        sha1obj = hashlib.md5()
        sha1obj.update(file.read())
        hashStr = (sha1obj.hexdigest()).upper()
        return hashStr


class CheckThread(threading.Thread):
    global g_finish_flag
    def __init__(self, url, plat):
        threading.Thread.__init__(self)
        self.url = url
        self.plat = plat
        self.taskList = []

    def timerQuest(self):
        global g_finish_flag
        if len(self.taskList) > 0:
            currTask = self.taskList[0]
            try:
                response = urllib2.urlopen(currTask["url"])
                data = response.read()
                myUtil.writeFile(BUFFER_DIR + "cache.data", data)
                cacheMd5 = calcMD5(BUFFER_DIR + "cache.data")
                if cacheMd5 == currTask["md5"]:
                    print("任务完成：" + currTask["url"])
                    self.taskList = self.taskList[1:]

            except:
                print("404 at " + currTask["url"])
                pass
        if len(self.taskList) > 0:
            time.sleep(10)
            self.timerQuest()
        else:
            g_finish_flag = 1


    def run(self):
        global lock, g_finish_flag
        lock.acquire()
        self.doCheck()
        lock.release()

    def doCheck(self):
        file = open(os.path.join(BUFFER_DIR, "config.info"), "rb")
        infoFile = open(os.path.join(BUFFER_DIR, "info.info"), "rb")
        line = file.readline()
        if line.find("config.json") > -1:
            self.doCheckConfigJson(infoFile)
        elif line.find("config_md5.json") > -1:
            self.doCheckConfigJson(infoFile)
        elif line.find("patch.info") > -1:
            self.doCheckPatchInfo(infoFile)
        elif line.find(".info") > -1 and (line[0:1] == "10" or line[0:4] == "level"):
            self.doCheckLevelInfo(infoFile)

        file.close()
        infoFile.close()

    def doCheckConfigJson(self, file):
        cfgJson = json.load(file)
        ver = cfgJson["configVersion"]

        platUrl = "android/3000/"
        if self.plat == "ios":
            platUrl = "ios/1/"

        md5url = self.url + platUrl + "config_ex/" + str(ver) + "/config_md5.json"
        #拿到md5.json
        while True:
            try:
                response = urllib2.urlopen(md5url)
                data = response.read()
                myUtil.writeFile(BUFFER_DIR + "config_md5.json", data)
                break
            except:
                time.sleep(30)
                pass

        cfgMd5Json = json.loads(myUtil.readFile(BUFFER_DIR + "config_md5.json"))
        for key in cfgMd5Json.keys():
            val = cfgMd5Json[key]
            #这次更新的配置
            if val["url"].find(str(ver)) == 0:
                requestUrl = self.url + platUrl + "config_ex/" + val["url"] + "?v=" + val["md5"]
                self.taskList.append({"url":str(requestUrl), "md5":val["md5"]})
        self.timerQuest()
        return

    def doCheckPatchInfo(self, file):
        global g_finish_flag
        ver = None
        md5 = None
        for line in file:
            print(line)
            l1 = line.split(':')
            if l1[0] == "ver":
                if l1[1][-1] == '\n':
                    ver = l1[1][0:-2]
                else:
                    ver = l1[1]
            elif l1[0] == "md5":
                if l1[1][-1] == '\n':
                    md5 = l1[1][0:-2]
                else:
                    md5 = l1[1]

        if ver and md5:
            platUrl = "android/3000/"
            if self.plat == "ios":
                platUrl = "ios/1/"
            requestUrl = self.url + platUrl + "update/" + str(ver) + "/patch.data?v=" + str(md5)
            print(type(requestUrl))
            self.taskList.append({"url":str(requestUrl), "md5":md5})
            self.timerQuest()
        else:
            g_finish_flag = -1

    def doCheckLevelInfo(self, file):
        global g_finish_flag
        level = None
        md5 = None
        for line in file:
            l1 = line.split(':')
            if l1[0] == "level":
                if l1[1][-1] == '\n':
                    level = l1[1][0:-2]
                else:
                    level = l1[1]
            elif l1[0] == "md5":
                if l1[1][-1] == '\n':
                    md5 = l1[1][0:-2]
                else:
                    md5 = l1[1]
    
        if level and md5:
            platUrl = "android/3000/"
            if self.plat == "ios":
                platUrl = "ios/1/"
            requestUrl = self.url + platUrl + "level/" + str(ver) + "/level.data?v=" + str(md5)
            print(type(requestUrl))
            self.taskList.append({"url":str(requestUrl), "md5":md5})
            self.timerQuest()

def runCheck(url, plat):
    global g_finish_flag
    if not url or not plat:
        g_finish_flag = -1
        return
    checkThread = CheckThread(url, plat)
    checkThread.start()

def isFinish():
    return g_finish_flag


if __name__ == "__main__":
    os.chdir("../")
    runCheck("http://vkdrpdla.pg-pobba4.cdn.emato.net/wdjt/", "android")
