import requests
import pygsheets
import os

# 获取user_access_token
path = os.getcwd() + '/docapi-304801-2301091b9dc2.json'
gc = pygsheets.authorize(service_file=path)
google_sheet = gc.open('🪁链接合集🎈')
sheet = google_sheet.worksheet_by_title('飞书API_token')
user_access_token = sheet.get_value('A2')
# 新建文档
url = 'https://open.feishu.cn/open-apis/doc/v2/create'
header = {'Authorization':'Bearer '+user_access_token,'Content-Type':'application/json; charset=utf-8'}
send_data = {'FolderToken':'fldcndDuqAuBUZ8HfvFd3cZ0vtL','Content':'sheet'}
title_name = '第一个api调用文档'
title_json = {"elements":[{"type":"textRun","textRun":{"text":title_name,"style":{"align": "center"}}}]}