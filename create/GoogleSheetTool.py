import requests
import json
import pygsheets

# 打开Google表格
def Get_google_sheets(name):
    path = 'C:/Python_test/Bytedance/docapi-304801-2301091b9dc2.json'
    gc = pygsheets.authorize(service_file=path)
    google_name = gc.open(name)
    return google_name