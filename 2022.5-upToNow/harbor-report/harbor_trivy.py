#! usr/bin/env python
#-*-coding=utf-8-*-

import json
import requests
import urllib.parse

PROJECT_LIST = []
REPO_LIST = []
CVE_LIST = []
VULNS = {
    'Critical': 0,
    'High':0,
    'MEDIUM':0,
    'LOW':0,
    'UNKNOWN':0
}

BASE_URL = "https://yourDomain.com"

def getProjects():  
    url = BASE_URL + "/api/v2.0/projects?page=1&page_size=-1&with_detail=false"  # -1可获取总量all
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'authorization': 'Basic YWRtaW46TGxzQGhhcmJvcjEyMw=='
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    if r.status_code == 200:
        content = json.loads(r.text)
    if len(content) :
        for d in content:
            if 'name' in d.keys() and 'repo_count' in d.keys() and d["repo_count"]:
                PROJECT_LIST.append(d["name"])
    print("Project count: ",len(PROJECT_LIST))
    
def getRepoByProname(proName):
    RepoList = []
    url = BASE_URL + "/api/v2.0/projects/" + proName + "/repositories?page=1&page_size=-1"  # -1可获取总量all
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'authorization': 'Basic YWRtaW46TGxzQGhhcmJvcjEyMw=='
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    if r.status_code == 200:
        content = json.loads(r.text)
        for r in content:
            if 'name' in r.keys():
                RepoList.append(r["name"])

def getRepos():
    getProjects()
    for p in PROJECT_LIST:
        url  = BASE_URL + "/api/v2.0/projects/" + p + "/repositories?page=1&page_size=-1"   # -1可获取总量all
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'authorization': 'Basic YWRtaW46TGxzQGhhcmJvcjEyMw=='
        }
        r = requests.get(url, headers=headers)
        r.encoding = "utf-8"
        if r.status_code == 200:
            content = json.loads(r.text)
            for r in content:
                REPO_LIST.append(r["name"])
        else:
            print("------------------- get reposBypname failed: ", p, " -------------------")  # images 会统计遗漏

    print("Repos count: ", len(REPO_LIST))

def splitRepo(repoName):
    result = repoName.split("/")
    pname = result[0]
    result.remove(result[0])
    if len(result) == 1:
        rname = result[0]
    else:
        rname = result[0]
        for i in range(len(result)):
            if i > 0:
                rname += urllib.parse.quote("%2f") + result[i]
    return pname,rname

def scanVul(pname, rname, sha):
    url = BASE_URL + "/api/v2.0/projects/" + pname + "/repositories/" + rname + "/artifacts/" + sha + "/scan"
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'authorization': 'Basic YWRtaW46TGxzQGhhcmJvcjEyMw=='
    }
    r = requests.post(url, headers=headers)
    r.encoding = "utf-8"
    if r.status_code == 202:
        print("=================== start scan success: ", pname, rname, sha, " ===================")
    else:
        print("------------------- start scan failed: ", pname, rname, sha, " -------------------")

def getCVE(pname, rname, sha):
    url = BASE_URL + "/api/v2.0/projects/" + pname + "/repositories/" + rname + "/artifacts/" + sha + "/additions/vulnerabilities"
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'authorization': 'Basic YWRtaW46TGxzQGhhcmJvcjEyMw=='
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    if r.status_code == 200:
        content = json.loads(r.text)
        cveDetails = list(content.values())[0]["vulnerabilities"]
        for cve in cveDetails:
            if cve["id"] not in CVE_LIST:
                CVE_LIST.append(cve["id"])
    else:
        print("------------------- getCVE failed: ", pname, rname, sha, " -------------------")

def getVulns():
    IMAGE_CNT = 0
    SAFE_IMAGE_CNT = 0
    SCAN_FAILED = 0
    UNSCAN_CNT = 0
    getRepos()
    for repo in REPO_LIST:
        pname,rname = splitRepo(repo)
        url = BASE_URL + "/api/v2.0/projects/" + pname + "/repositories/" + rname + "/artifacts?page=1&page_size=-1&with_scan_overview=true"   # -1可获取总量all
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'authorization': 'Basic YWRtaW46TGxzQGhhcmJvcjEyMw=='
        }
        r = requests.get(url, headers=headers)
        r.encoding = "utf-8"
        if r.status_code == 200:
            content = json.loads(r.text)
            for img in content:
                if "digest" in img.keys():
                    artiSHA = img["digest"]
                    IMAGE_CNT += 1
                else:
                    print("------------------- no digest: -------------------") # images 会统计遗漏
                if "scan_overview" in img.keys() : # 已扫描
                    dVul = list(img["scan_overview"].values())[0]
                    if dVul["scan_status"] == "Success": #扫描成功
                        if dVul["summary"]["total"] > 0: # 扫描成功且有漏洞
                            getCVE(pname, rname, artiSHA) # 统计不重复的cve
                            dtmp = dVul["summary"]["summary"]
                            if 'Critical' in dtmp.keys():
                                VULNS['Critical'] += dtmp['Critical']
                            if 'High' in dtmp.keys():
                                VULNS['High'] += dtmp['High']
                            # print(dVul["summary"]["summary"])
                        else: # 没有漏洞的统计
                            SAFE_IMAGE_CNT += 1
                    else: # 扫描失败
                        SCAN_FAILED += 1
                        scanVul(pname, rname, artiSHA)
                else: # 未扫描
                    UNSCAN_CNT += 1
                    scanVul(pname, rname, artiSHA)
        else:
            print("------------------- get artifacts failed by repo: ", pname, rname, "-------------------") # images 会统计遗漏

    print("image count: ", IMAGE_CNT)
    print("safe image count: ", SAFE_IMAGE_CNT)
    print("scan failed count: ", SCAN_FAILED)
    print("unscan count: ", UNSCAN_CNT)
    print("CVE count: ", len(CVE_LIST))
    print("vulns count: ", VULNS)


if __name__ == "__main__":
    getVulns()
    #getCVE("zjszjr", "zjszjr-limit-service", "sha256:255df43ed3ff693c38fa61d03bb2539c11d5e555ee41d561a52cd87f2e03f4bd")