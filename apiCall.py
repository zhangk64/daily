#! usr/bin/env python
#-*-coding=utf-8-*-
import json
from requests_toolbelt import MultipartEncoder
import requests

API_KEY = "XFFoH6tMWILlJQ5UOa5jR6nTIi9CuwFa"
# API_KEY = "pDn8daOSmQGUQ1m66wFocUkfl4yfScPQ"
BASE_URL = "http://172.16.184.48:8080/api"
# BASE_URL = "http://dependency-track.lls.com/api"
PRE_DIR = "target/"

# 新建项目
def createProject(pname, pver):
    result = False
    pid = ""
    url = BASE_URL + "/v1/project"
    try:
        header = {
            'X-Api-Key': API_KEY,
            'Content-Type' : 'application/json',
            'Origin': 'http://172.16.184.48:8080'
            # 'Origin': 'http://dependency-track.lls.com'
        }
        data = {
            'name': pname,
            'version': pver
        }
        r = requests.put(url, headers=header, data=json.dumps(data))
        r.encoding = "utf-8"
        if r.status_code == 201:
            result = True
            re_dict = json.loads(r.text)
            pid = re_dict["uuid"]
            return result, pid
    except Exception as e:
        print("Failed createProject: " + str(e))
    return result, None

# 上传bom文件
def uploadBom(pid, fname):
    result = False
    url = BASE_URL + "/v1/bom"
    try:
        data = MultipartEncoder(
            fields={
                'project' : pid,
                'bom' : ('test.json', open(PRE_DIR + fname, 'rb'), 'application/json')
            }
        ) 
        header = {
            'X-Api-Key': API_KEY,
            'Content-Type': data.content_type
        }
        r = requests.post(url, headers=header, data=data)
        r.encoding = "utf-8"
        if r.status_code == 200:
            result = True
            return result
    except Exception as e:
        print("Failed uploadBom: " + str(e))
    return result


if __name__ == "__main__":
    # uploadBom("33a6b036-6f80-4bbf-b7dd-e27876a63610", 'bom.xml')
    pass 