import requests
import json
import pygsheets
import os

# 获取app_access_token
# app_id = 'cli_a0912bb0e939900d'
# app_secret = 'hwS7c7MMc6Nq0QrdvfIrobU0D2xWRLlh'
app_id = 'cli_a0912bb0e939900d'
app_secret = '5oZVQKPERYmfCMXjzYljHfmqG4TLdYBh'
app_url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
header = {'Content-Type':'application/json; charset=UTF-8'}
send_data = {'app_id':app_id,'app_secret':app_secret}
r = requests.post(url=app_url,headers=header,data=json.dumps(send_data)).text
print(r)
app_access_token = json.loads(r)['app_access_token']

# 获取code 程序登陆，network获取
code = '36asfcb169f1491781d8a352baba4727'

# 获取user_access_token
user_url = 'https://open.feishu.cn/open-apis/authen/v1/access_token'
header = {'Authorization':'Bearer '+app_access_token,'Content-Type':'application/json; charset=UTF-8'}
send_data = {
    "grant_type": "authorization_code",
    "code": code
}
r = requests.post(url=user_url,headers=header,data=json.dumps(send_data)).text
user_access_token = json.loads(r).get('data').get('access_token')
refresh_token = json.loads(r).get('data').get('refresh_token')

# 将access_token、refresh_token 写在Google表中，便于刷新使用
google_name = '🪁链接合集🎈'
# authorization
path = os.getcwd()+'//docapi-304801-2301091b9dc2.json'
gc = pygsheets.authorize(service_file=path)
google_sheet = gc.open(google_name)

sheet = None
for sheet_name in google_sheet.worksheets():
    if sheet_name.title == '飞书API_token':
        sheet = sheet_name
sheet.update_value('A4',user_access_token)
sheet.update_value('B4',refresh_token)