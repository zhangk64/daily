#! usr/bin/env python
#-*-coding=utf-8-*-

import os
import json
import sys
import requests
import datetime
from datetime import datetime
import json
import pandas as pd
from  datetime import datetime, timedelta


API_KEY = "pDn8daOSmQGUQ1m66wFocUkfl4yfScPQ"
BASE_URL = "http://dependency-track.lls.com/api"

def getPid():
    pid_list = {}
    url = "http://dependency-track.lls.com/api/v1/project?excludeInactive=true&searchText=&sortName=lastBomImport&sortOrder=asc&pageSize=80&pageNumber=1"
    try:
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
            'X-Api-Key': API_KEY
        }
        r = requests.get(url, headers=header)
        r.encoding = "utf-8"
        if r.status_code == 200:
            content = json.loads(r.text)
            for p in content:
                if p["lastInheritedRiskScore"] == 0:
                    print(p["uuid"])
                    delete_project(p["uuid"])
            #pids = content["results"]["project"]
            #for tmp in pids:
                #pid_list[tmp["uuid"]] = [tmp["name"]]

        else:
            print("getPid failed.", r.status_code)
    except Exception as e:
        print("Failed getPid: " + str(e))
    return pid_list

# 获取报告信息
def delete_project(pid):
    if pid == "":
        return 
    report_data = []
    url = BASE_URL + "/v1/project/" + str(pid) 
    try:
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
            'X-Api-Key': API_KEY
        }
        r = requests.delete(url, headers=header)
        r.encoding = "utf-8"
        content = r.text
        print(r.status_code)
    except Exception as e:
        print("Failed request_report: " + str(e))
    return report_data



if __name__ == "__main__":
    getPid()
    #readFile()