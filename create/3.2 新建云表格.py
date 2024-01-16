import requests
import pygsheets
import os
import json

# 获取user_access_token
path = os.getcwd() + '/docapi-304801-2301091b9dc2.json'
gc = pygsheets.authorize(service_file=path)
google_sheet = gc.open('🪁链接合集🎈')
sheet = google_sheet.worksheet_by_title('飞书API_token')
user_access_token = sheet.get_value('A2')
# 新建文档
title_name = '第一个api生成文档'
url = 'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets'
header = {'Authorization':'Bearer '+user_access_token,'Content-Type':'application/json; charset=utf-8'}
send_data = {'folder_token':'fldcndDuqAuBUZ8HfvFd3cZ0vtL',"title":title_name}

r = requests.post(url=url,headers=header,data=json.dumps(send_data)).text
print(json.loads(r))