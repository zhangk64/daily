#! usr/bin/env python
#-*-coding=utf-8-*-

import os
from apiCall import *
from report2excel import *

DIR = os.path.dirname(os.path.realpath(__file__)) + "\\target"
VERSION = "20240113"

# 遍历文件
def readFile():
    for root, dirs, files in os.walk(DIR):
        for file in files:
            fname, fsuffix = os.path.splitext(file)
            succ, pid = createProject(fname, VERSION)
            if succ == True:
                print(file, pid, "createPro success.")
                uploadFlag = uploadBom(pid, file)
                if uploadFlag == True:
                    print(file, "upload success.")
                else:
                    print(file, "upload failed................................................")
            else:
                print(file, "createPro failed................................................")


if __name__ == "__main__":
    readFile()
    pass