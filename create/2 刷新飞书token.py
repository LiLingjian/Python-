import requests
import json
import os
import pygsheets

# 获取保存的refresh_token
google_name = '🪁链接合集🎈'
path = os.getcwd()+'//docapi-304801-2301091b9dc2.json'
gc = pygsheets.authorize(service_file=path)
google_sheet = gc.open(google_name)
sheet = google_sheet.worksheet_by_title('飞书API_token')
# user_access_token = sheet.get_value('A2')
refresh_token = sheet.get_value('B2')

# 获取app_access_token
app_id = 'cli_a0912bb0e939900d'
app_secret = 'hwS7c7MMc6Nq0QrdvfIrobU0D2xWRLlh'
app_url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
header = {'Content-Type':'application/json; charset=UTF-8'}
send_data = {'app_id':app_id,'app_secret':app_secret}
r = requests.post(url=app_url,headers=header,data=json.dumps(send_data)).text
app_access_token = json.loads(r)['app_access_token']

# 刷新token
url = 'https://open.feishu.cn/open-apis/authen/v1/refresh_access_token'
header = {'Authorization':'Bearer '+app_access_token,'Content-Type':'application/json; charset=utf-8'}
send_data = {'grant_type':'refresh_token','refresh_token':refresh_token}
r = requests.post(url=url,headers=header,data=json.dumps(send_data)).text
user_access_token = json.loads(r).get('data').get('access_token')
refresh_token = json.loads(r).get('data').get('refresh_token')
sheet.update_value('A2',user_access_token)
sheet.update_value('B2',refresh_token)