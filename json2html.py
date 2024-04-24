#! usr/bin/env python
#-*-coding=utf-8-*-

import json
import json2html
from  json2html import *

dict_str = open('test.json','r',encoding='utf-8').read()
data_dict = json.loads(dict_str)
#data_xml = json2html.convert(json = data_dict)
data_xml = json2html.convert(json=data_dict, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
print("data_xml", data_xml)
html_head = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{}
</body>
</html>'''
result_html = html_head.format(data_xml)

with open('test.html','w',encoding='utf-8') as file:
    file.write(result_html)


