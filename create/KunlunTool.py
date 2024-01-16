import requests
import json

# 获取应用 Token，有效期2小时。
def get_kunlun_token():
    url = 'https://ae-openapi.feishu.cn/auth/v1/appToken'
    headers = {'Content-Type':'application/json'}
    payload = {'clientId':'c_af420d8a357849399ed8','clientSecret':'a472b1cf772443ec96c0cc2b830fd2ce'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)['data']['accessToken']

# 查询实时diff同步记录列表，https://apaas.feishuapp.cn/ae/ui/setup/appPackages/package_copyjta2n__c/openApiManagement/document/record-object_shishidiff-getRecords
def get_kunlundiff_info(payload):
    token = get_kunlun_token()
    url = "https://ae-openapi.feishu.cn/api/data/v1/namespaces/package_copyjta2n__c/objects/object_shishidiff/records"
    headers = {
      "Authorization": token,
      "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)


# 新增数据
def append_kunlundiff_info(payload):
    token = get_kunlun_token()
    url = "https://ae-openapi.feishu.cn/api/data/v1/namespaces/package_copyjta2n__c/objects/object_shishidiff"
    headers = {
      "Authorization": token,
      "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)

# 批量新建实时diff同步记录  https://apaas.feishuapp.cn/ae/ui/setup/appPackages/package_copyjta2n__c/openApiManagement/document/record-object_shishidiff-batchCreateRecords
def batch_append_kunlundiff_info(payload):
    token = get_kunlun_token()
    url = "https://ae-openapi.feishu.cn/api/data/v1/namespaces/package_copyjta2n__c/objects/object_shishidiff/batchCreate"
    headers = {
      "Authorization": token,
      "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)

# 一次编辑多条实时diff同步记录  https://apaas.feishuapp.cn/ae/ui/setup/appPackages/package_copyjta2n__c/openApiManagement/document/record-object_shishidiff-batchUpdateRecords
def batchUpdate_diff_info(payload):
    token = get_kunlun_token()
    url = "https://ae-openapi.feishu.cn/api/data/v1/namespaces/package_copyjta2n__c/objects/object_shishidiff/batchUpdate"
    headers = {
      "Authorization": token,
      "Content-Type": "application/json"
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)

# 批量删除实时diff同步记录，https://apaas.feishuapp.cn/ae/ui/setup/appPackages/package_copyjta2n__c/openApiManagement/document/record-object_shishidiff-batchDeleteRecords
def del_diffcase(payload):
    token = get_kunlun_token()
    url = "https://ae-openapi.feishu.cn/api/data/v1/namespaces/package_copyjta2n__c/objects/object_shishidiff/batchDelete"
    headers = {
      "Authorization": token,
      "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)