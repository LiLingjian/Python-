import requests
import pygsheets
import json
import os


# 打开Google表格
def get_google_sheets(name):
    # path = os.getcwd() + '/docapi-304801-2301091b9dc2.json'
    path = 'C:/Python_test/Bytedance/docapi-304801-2301091b9dc2.json'
    gc = pygsheets.authorize(service_file=path)
    google_name = gc.open(name)
    return google_name

# 获取存放在Google表中的飞书user_access_token
def get_user_access_token():
    google_name = get_google_sheets('🪁链接合集🎈')
    sheet = google_name.worksheet_by_title('飞书API_token')
    return sheet.get_value('A2')

# 新建文档，默认放在我的那个文件夹里
def set_docs(content,FolderToken='fldcndDuqAuBUZ8HfvFd3cZ0vtL'):
    user_access_token = get_user_access_token()
    url = 'https://open.feishu.cn/open-apis/doc/v2/create'
    header = {'Authorization':'Bearer '+user_access_token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {"FolderToken":FolderToken,"Content":json.dumps(content)}
    r = requests.post(url=url,headers=header,data=json.dumps(send_data)).text
    # return json.loads(r)
    docToken = json.loads(r)['data']['objToken']
    doc_url = json.loads(r)['data']['url']
    return docToken,doc_url

# 获取doc内sheet的元数据，返回sheetToken、sheetId等
def get_doc_sheetId(docToken):
    access_token = get_user_access_token()
    url = f'https://open.feishu.cn/open-apis/doc/v2/{docToken}/sheet_meta'
    header = {'Authorization':'Bearer ' + access_token,'Content-Type':'application/json; charset=utf-8'}
    r = requests.get(url=url,headers=header).text
    return json.loads(r)

# 为飞书文档/表格增加权限，并有【添加权限后是否通知对方】的功能，https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/permission-member/create
def doc_notification(docToken,email):
    access_token = get_user_access_token()
    url = f'https://open.feishu.cn/open-apis/drive/v1/permissions/{docToken}/members'
    header = {'Authorization':'Bearer ' + access_token,'Content-Type':'application/json; charset=utf-8'}
    params = {'type':'doc', 'need_notification':True}
    send_data = {'member_type':'email', 'member_id':email, 'perm':'view'}
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data)).text
    return json.loads(r)

