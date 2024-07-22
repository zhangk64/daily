'''
import datetime

from datetime import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')
print(type(current_date),current_date)

# 当前时间的年月日
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day
 
print(f"year: {year}, month: {month}, day: {day}")
'''
# 虾推啥  
# 注：每日上限500次，每分钟上限10次，单ip每日http请求上限5000次
import requests

mydata={
'text':'预警，test2405<10000！预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警预警',
'desp':''
}

requests.post('http://wx.xtuis.cn/eYyuUBYp9t9XOjTvqKVlKXQda.send', data=mydata)     