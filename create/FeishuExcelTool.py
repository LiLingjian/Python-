import requests
import json
import pygsheets

#飞书工具类
#获取飞书sheets信息
#ranges = "b70158!A1:D10"

# 打开Google表格
def Get_google_sheets(name):
    path = 'C:/Python_test/Bytedance/docapi-304801-2301091b9dc2.json'
    gc = pygsheets.authorize(service_file=path)
    google_name = gc.open(name)
    return google_name

# 获取存放在Google表中的飞书user_access_token
def Get_feishu_token():
    google_name = Get_google_sheets('🪁链接合集🎈')
    sheet = google_name.worksheet_by_title('飞书API_token')
    return sheet.get_value('A2')

# 读取飞书sheet的内容
def Get_sheets_info(spreadsheetToken,ranges,valueRenderOption='ToString',dateTimeRenderOption='FormattedString'):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values_batch_get'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    params = {'ranges':ranges,'valueRenderOption':valueRenderOption,'dateTimeRenderOption':dateTimeRenderOption}
    r = requests.get(url=url,headers=header,params=params).text
    data_json = json.loads(r).get('data').get('valueRanges')[0].get('values')
    return data_json

# 该接口用于获取电子表格下所有工作表及其属性，https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/sheets-v3/spreadsheet-sheet/query
def get_sheetID(spreadsheetToken):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheetToken}/sheets/query'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    r = requests.get(url=url,headers=header).text
    data_json = json.loads(r).get('data').get('sheets')
    return data_json

# 增加工作表
def add_sheet(spreadsheetToken,title,index=0):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/sheets_batch_update'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
      "requests": [
        {
          "addSheet": {
            "properties": {
              "title": title, # 标题
              "index": index  # 位置,不填默认往前增加工作表
            }
          }
        }
      ]
    }
    r = requests.post(url=url,headers=header,data=json.dumps(send_data)).text
    sheetId = json.loads(r).get('data').get('replies')[0].get('addSheet').get('properties').get('sheetId')
    return sheetId

# 复制工作表，要copy的sheetID，复制后的新表名
def copy_sheet(spreadsheetToken,old_sheetId,title):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/sheets_batch_update'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
      "requests": [
          {
              "copySheet": {
                  "source": {
                      "sheetId": old_sheetId
                  },
                  "destination": {
                      "title": title
                  }
              }
          }
      ]
    }
    r = requests.post(url=url,headers=header,data=json.dumps(send_data)).text
    sheetId = json.loads(r).get('data').get('replies')[0].get('addSheet').get('properties').get('sheetId')
    return sheetId


# 往飞书表内插入数据,注，插入的是行
def Insert_sheets_info(spreadsheetToken,range,values):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values_prepend'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {'valueRange':{'range':range,'values':values}}
    r = requests.post(url=url,headers=header,data=json.dumps(send_data))
    return r.text

# 往飞书表内追加数据，以A列第一个为空的单元格，插入式追加，（追加多少行，总行数增加多少行）,
# https://open.feishu.cn/document/ukTMukTMukTM/uMjMzUjLzIzM14yMyMTN
def Append_sheets_info(spreadsheetToken,send_data):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values_append'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    params = {'insertDataOption': 'INSERT_ROWS'}
    # send_data = {'valueRange':{'range':range,'values':values}}
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data))
    return r.text

# 往飞书表内追加数据，以A列第一个为空的单元格，插入式追加，（追加多少行，总行数增加多少行）
# https://open.feishu.cn/document/ukTMukTMukTM/uMjMzUjLzIzM14yMyMTN
def Append_sheets_info_notinsert(spreadsheetToken,send_data):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values_append'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    params = {'insertDataOption': 'OVERWRITE'}
    # send_data = {'valueRange':{'range':range,'values':values}}
    r = requests.post(url=url,headers=header,params=params,data=json.dumps(send_data))
    return r.text

# 向多个范围写入数据
def Write_sheets_info(spreadsheetToken,send_data):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values_batch_update'
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json; charset=utf-8'}
    # send_data = {
    #     "valueRanges": [
    #         {
    #             "range": feishu_ranges,
    #             "values": values
    #         },
    #         # {
    #         #   "range": 'I36El2',
    #         #   "values": data_banci
    #         # }
    #     ]
    # }
    r = requests.post(url=url, headers=header, data=json.dumps(send_data))
    return r.text

# 删除飞书sheet的行列
def Del_sheets_info(spreadsheetToken,sheetId,startIndex,endIndex):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/dimension_range'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {'dimension':{'sheetId':sheetId,'majorDimension':'ROWS','startIndex':startIndex,'endIndex':endIndex}}
    r = requests.delete(url=url,headers=header,data=json.dumps(send_data))
    return r.text

# 设置单元格样式，如字体，颜色，居中等
def set_sheet_format(spreadsheetToken,send_data):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/style'
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json; charset=utf-8'}
    # send_data = https://open.feishu.cn/document/ukTMukTMukTM/ukjMzUjL5IzM14SOyMTN
    r = requests.put(url=url, headers=header, data=json.dumps(send_data))
    return r.text

# 插入行列,一般用于删除，因为删除时超出了sheet所有范围会报错，所以先插入再删除
def insert_rows(spreadsheetToken,sheetId,startIndex,endIndex):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/insert_dimension_range'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
            "dimension":{
                "sheetId":sheetId,
                "majorDimension":"ROWS",
                "startIndex":startIndex,
                "endIndex":endIndex
            }
        }
    r = requests.post(url=url,headers=header,data=json.dumps(send_data))
    return r.text

# 增加行列,一般用于删除，因为删除时超出了sheet所有范围会报错，所以先增加再删除
def add_rows(spreadsheetToken,sheetId,num):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/dimension_range'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
          "dimension":{
               "sheetId": sheetId,
                "majorDimension": "ROWS",
                "length": num
             }
        }
    r = requests.post(url=url,headers=header,data=json.dumps(send_data))
    return r.text

# 更新行列，一般用于隐藏行列，也能设置行列宽
def hide_rows(spreadsheetToken,sheetId,majorDimension,startIndex,endIndex):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/dimension_range'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
        "dimension":{
            "sheetId":sheetId,
            "majorDimension":majorDimension,
            "startIndex":startIndex,
            "endIndex":endIndex
        },
        "dimensionProperties":{
            "visible":False,
            # "fixedSize":50
        }
    }
    r = requests.put(url=url,headers=header,data=json.dumps(send_data))
    return r.text

# 获取工作表，给文档token，返回sheetID和title https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/query
def get_sheetsID_title(spreadsheetToken):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheetToken}/sheets/query'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    r = requests.get(url=url,headers=header)
    return r.text

# 清楚单元格内容，新版的功能，试一下，https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet-value/batch_clear
def clear_ranges(spreadsheet_token,sheet_id,range=''):
    token = Get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/values/batch_clear'
    header = {'Authorization':'Bearer '+token,'Content-Type':'application/json; charset=utf-8'}
    send_data = {
        "ranges": [
            sheet_id+range
        ]
    }
    r = requests.post(url=url,headers=header,data=json.dumps(send_data))
    return r.text