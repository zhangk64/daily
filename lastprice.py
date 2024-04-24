#! usr/bin/env python
#-*-coding=utf-8-*-

import os
import json
import requests
import threading
import tkinter as tk

CODE = "113.hc2410,113.rb2410,115.FG409,115.SA409"  # stock code, ep: 114.cs2403,114.c2405

class TestGUI:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True) # del menu bar
        self.root.attributes("-alpha", 0.4) # window transparency 60%
        self.root.attributes("-topmost", True) # window top
        self.label = tk.Label(root, text="")
        self.label.pack()

        # no use system proxy 
        os.environ['NO_PROXY'] = 'push2.eastmoney.com' 

        # create thread
        self.thread = threading.Thread(target=self.update_label)
        self.thread.daemon = True

        # start thread 
        self.thread.start()
        
    def update_label(self):
        while True:
            try:
                text = self.getPrice()
            except Exception as e:
                text = str(e)
            self.label.config(text=text)


    def getPrice(self):
        text = ""
        # origin url https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f12,f13,f19,f14,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100,f88,f153&secids=114.cs2403,114.c2405,113.ru2405,114.fb2401
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
        params = {
            "fltt": "2",
            "fields": "f2",
            "secids": CODE
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        r = requests.get(url, params=params, headers=headers)
        r.encoding = "utf-8"
        content = json.loads(r.text)
        if "data" in content and content["data"] is not None and "diff" in content["data"]:
            price_list = content["data"]["diff"]
            for p in price_list:
                if p is not None and "f2" in p:
                    if text == "":
                        text = str(p['f2'])
                    else:
                        text += "," + str(p['f2'])
        return text


        
if __name__ == "__main__":
    root = tk.Tk()
    gui = TestGUI(root)
    root.mainloop()