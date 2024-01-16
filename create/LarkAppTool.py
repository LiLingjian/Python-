import requests
import json

# 获取app_access_token
def get_app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    header = {'Content-Type':'application/json; charset=utf-8'}
    send_data = {'app_id':'cli_a0912bb0e939900d','app_secret':'hwS7c7MMc6Nq0QrdvfIrobU0D2xWRLlh'}

    r = requests.post(url,headers=header,data=json.dumps(send_data))
    return json.loads(r.text)['app_access_token']

# 通过邮箱给个人推送消息
def send_messageToEmail(message,email):
    access_token = get_app_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    header = {'Authorization':'Bearer '+access_token,'Content-Type':'application/json; charset=utf-8'}
    params = {'receive_id_type':'email'}
    send_data ={
        'receive_id': email,
        'content': json.dumps(message),
        'msg_type': 'text'
    }
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data))
    return r.text

# 给群推送消息
def send_messageToChat(message,chat_id):
    access_token = get_app_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    header = {'Authorization':'Bearer '+access_token,'Content-Type':'application/json; charset=utf-8'}
    params = {'receive_id_type':'chat_id'}
    send_data ={
        'receive_id': chat_id,
        'content': json.dumps(message),
        'msg_type': 'text'
    }
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data))
    return r.text

# 给个人推送卡片消息
def send_cardmessageToEmail(content,email):
    access_token = get_app_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    header = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json; charset=utf-8'}
    params = {'receive_id_type': 'email'}
    send_data = {
        'receive_id': email,
        'content': json.dumps(content),
        'msg_type': 'interactive'
    }
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data))
    return r.text

# 通过群的名称，获取群id，https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/list
def get_chat_id(chat_name):
    access_token = get_app_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/chats'
    header = {'Authorization': 'Bearer ' + access_token}
    params = {
        'page_size':100
    }
    r = requests.get(url=url, headers=header,params=params)
    items = json.loads(r.text).get('data').get('items')
    for i in items:
        if i['name'] == chat_name:
            return i['chat_id']
    return '未找到此群，请检查名称是否正确'


# 给群推送卡片消息  https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
def send_cardmessageToChat(content: object, chat_id: object) -> object:
    access_token = get_app_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    header = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json; charset=utf-8'}
    params = {'receive_id_type': 'chat_id'}
    send_data = {
        'receive_id': chat_id,
        'content': json.dumps(content),
        'msg_type': 'interactive'
    }
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data))
    return r.text

# 通过手机号或邮箱获取用户 ID
def get_open_id(email):
    access_token = get_app_access_token()
    url = f'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id'
    header = {'Authorization':'Bearer ' + access_token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
            "emails": [email + "@jiyunhudong.com"]
        }
    r = requests.post(url=url,headers=header,data=json.dumps(send_data)).text
    # open_id = json.loads(r)['data']['user_list'][0]['user_id']
    open_id = json.loads(r)
    return open_id

# 获取群成员列表
def get_chat_members(chat_id):
    access_token = get_app_access_token()
    url = f'https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members'
    header = {'Authorization': 'Bearer ' + access_token,'Content-Type':'application/json; charset=utf-8'}

    r = requests.get(url=url, headers=header)
    members = json.loads(r.text)
    return members

# 上传图片
def upload_image(image_path):
    """上传图片
    Args:
        image_path: 文件上传路径
        image_type: 图片类型
    Return
        {
            "ok": true,
            "image_key": "xxx",
            "url": "https://xxx"
        }
    Raise:
        Exception
            * file not found
            * request error
    """

    access_token = get_app_access_token()
    url = 'https://open.feishu.cn/open-apis/image/v4/put/'
    header = {'Authorization':'Bearer ' + access_token}

    with open(image_path, 'rb') as f:
        image = f.read()
    resp = requests.post(
        url=url,
        headers=header,
        files={
            "image": image
        },
        data={
            "image_type": "message"
        },
        stream=True)


    resp.raise_for_status()
    content = resp.json()
    print(content)
    if content.get("code") == 0:
        return content
    else:
        raise Exception("Call Api Error, errorCode is %s" % content["code"])

# import os
# path = os.getcwd() + '\\裴钱.jpg'
# upload_image(path)

# 消息应用内加急
# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/urgent_app
def urgent_app(message_id,user_id):
    access_token = get_app_access_token()
    url = f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/urgent_app'
    header = {'Authorization': 'Bearer ' + access_token,'Content-Type':'application/json; charset=utf-8'}
    params = {'user_id_type': 'open_id'}
    send_data = {
        "user_id_list": [
            user_id
        ]
    }
    r = requests.patch(url=url, headers=header,params=params,data=json.dumps(send_data))
    return json.loads(r.text)