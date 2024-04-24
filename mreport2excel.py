#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import requests
import datetime
from datetime import datetime
import json
import os
import pandas as pd
from  datetime import datetime, timedelta

# curl -X 'GET'   'http://172.16.184.48:8080/api/v1/finding/project/e940f99c-59df-4ae2-8bb9-2c36d88959f2'   -H 'accept: application/json'   -H 'X-Api-Key: XFFoH6tMWILlJQ5UOa5jR6nTIi9CuwFa'
API_KEY = "XFFoH6tMWILlJQ5UOa5jR6nTIi9CuwFa"
API_GET_REPORT_PROID = ""
VUL_LEVEL = {"CRITICAL":"严重", "HIGH":"高危","MEDIUM":"中危", "LOW":"低危"}
DIR = os.path.dirname(os.path.realpath(__file__)) + "\\target"
BASE_URL = "http://172.16.184.48:8080/api"
VERSION = "20240113"

# 获取项目id
def  getPid(pname, pversion):
    pid = ""
    url = BASE_URL + "/v1/project/lookup"
    try:
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
            'X-Api-Key': API_KEY
        }
        data = {
            'name': pname,
            'version': pversion  
        }
        r = requests.get(url, headers=header, params=data)
        r.encoding = "utf-8"
        if r.status_code == 200:
            content = json.loads(r.text)
            #print(content["uuid"])
            pid = content["uuid"]
        else:
            print("getPid failed.", r.status_code)
    except Exception as e:
        print("Failed getPid: " + str(e))
    return pid

# 获取报告信息
def request_report(pid):
    if pid == "":
        return 
    report_data = []
    url = BASE_URL + "/v1/finding/project/" + str(pid) 
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
        content = r.text
        #print(content)
        report_data = json.loads(content)
    except Exception as e:
        print("Failed request_report: " + str(e))
    return report_data

# 获取表格数据
def gen_excel_data():
    excel_data = []
    try:
        for root, dirs, files in os.walk(DIR):
            for file in files:
                fname, fsuffix = os.path.splitext(file)
                #print(fname)
                pid = getPid(fname, VERSION)
                if pid is not None:
                    report_data  = request_report(pid)
                for i in range(len(report_data)):
                    tmp = report_data[i]
                    # print(tmp["component"])
                    vulLevel = tmp["vulnerability"]["severity"]
                    if vulLevel == "CRITICAL" or vulLevel == "HIGH": # 目前只处理严重和高危
                        if vulLevel in VUL_LEVEL.keys():
                            vLevel = VUL_LEVEL[vulLevel]
                        else:
                            vLevel = "未知"
                        tmp_vulInfo = [fname, tmp["component"]["name"], tmp["component"]["version"],"", tmp["component"]["purl"], tmp["vulnerability"]["vulnId"], vLevel, tmp["vulnerability"]["description"]]
                        #print(tmp_vulInfo)
                        excel_data.append(tmp_vulInfo)
        return excel_data
    except Exception as e:
        print("gen_excel_data: " + str(e))
    return excel_data


# 调整Excel报告格式
def modify_excel_format(excel_data, writer, df):
    # 调整excel格式 
    workbook = writer.book
    fmt = workbook.add_format({"font_name": u"宋体"})
    header_fmt = workbook.add_format(
        {'bold': True, 'font_size': 14, 'font_name': u'黑体', 'border': 1, 'bg_color': '#FFB400','font_color': 'black',
         'valign': 'vcenter', 'align': 'center'})
    header_fmt_sec_color = workbook.add_format(
        {'bold': True, 'font_size': 14, 'font_name': u'黑体', 'border': 1, 'bg_color': '#00B04E','font_color': 'black',
         'valign': 'vcenter', 'align': 'center'})
    detail_fmt = workbook.add_format(
        {"font_name": u"宋体", 'border': 0, 'valign': 'vcenter', 'align': 'left','font_size': 12, 'text_wrap': True})
    worksheet1 = writer.sheets['漏洞报告']
    for col_num, value in enumerate(df.columns.values):
        if col_num == 3:
            worksheet1.write(0, col_num, value, header_fmt_sec_color)
        else:
            worksheet1.write(0, col_num, value, header_fmt)
    # 设置列宽行宽
    worksheet1.set_column('A:B', 30, fmt)
    worksheet1.set_column('C:D', 20, fmt)
    worksheet1.set_column('E:E', 50, fmt)
    worksheet1.set_column('F:F', 20, fmt)
    worksheet1.set_column('G:G', 12, fmt)
    worksheet1.set_column('H:H', 80, fmt)
    worksheet1.set_row(0, 30, fmt)
    for i in range(1, len(excel_data)+1):
        worksheet1.set_row(i, 27, detail_fmt)

# 生成Excel
def gen_excel(pname):
    if pname == "":
        return 
    excel_data = gen_excel_data()
    if len(excel_data) == 0:
        print("excel_data is None!")
        return 
    columns = ["模块名称", "组件名称", "版本号", "建议版本", "包路径", "漏洞编号", "漏洞等级", "漏洞详细"]
    try:
        df = pd.DataFrame(data=excel_data, columns=columns)
        current_date = datetime.now().strftime('%Y%m%d')
        excel_name = '组件安全检查报告(高危版)-%s%s-%s.xlsx' % (pname, VERSION, current_date)
        with pd.ExcelWriter(path=excel_name, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name='漏洞报告', index=False)
            modify_excel_format(excel_data, writer, df)
        print("get_excel success: %s" % excel_name)
    except Exception as e:
        print("get_excel: " + str(e))

# 统计漏洞数量
def countVul():
    cnt = 0
    for root, dirs, files in os.walk(DIR):
        for file in files:
            fname, fsuffix = os.path.splitext(file)
            #print(fname)
            pid = getPid(fname, VERSION)
            if pid is not None:
                report_data  = request_report(pid)
            for i in range(len(report_data)):
                tmp = report_data[i]
                # print(tmp["component"])
                vulLevel = tmp["vulnerability"]["severity"]
                cnt += 1
    return cnt
        


if __name__ == "__main__":
    try:
        fname = sys.argv[1] # 项目名称
        print("总漏洞数： %d." % countVul())
        gen_excel(fname)
    except Exception as e:
        print("请输入参数！fname")
