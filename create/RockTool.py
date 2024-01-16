import requests
import json
# import datetime
from Bytedance.Tools.FeishuExcelTool import Get_google_sheets,Get_sheets_info


# 初判未处理，田康的cookie
def validator_not_deal(new_audit_time,origin_verifier):
    # 实时diff，1小时查询一次（抽检审出时间），以初审人分割，不可能diff>10条，不用调整end=10
    cookie = Get_sheets_info('shtcnDIedThxxQGVV8tHGk0Ug5f', 'BFaFLt')[1][1]
    header = {"cookie": cookie, 'content-type': 'text/plain; charset=utf-8'}
    url = f'https://rock.bytedance.net/api/v2/appealCaseList'
    params = {
        'verifier_type': 5,  # 0-初审/代操作，5-初判
        'case_state': 0,  # 0-待处理，2-已处理
        'search_value_enum': 0,
        'new_audit_time': new_audit_time,
        'order_field': 'remain_time',
        'order': 0,
        'origin_verifier': origin_verifier,
        'start': 0,
        'end': 20,
    }
    r = requests.get(url=url, params=params, headers=header).text
    return json.loads(r)

# 初判已处理，返回处理结果，田康的cookie
def validator_dealed_result(origin_audit_time,origin_verifier):
    # 实时diff，1小时查询一次（抽检审出时间），以初审人分割，不可能diff>10条，不用调整end=10
    cookie = Get_sheets_info('shtcnDIedThxxQGVV8tHGk0Ug5f', 'BFaFLt')[1][1]
    header = {"cookie": cookie, 'content-type': 'text/plain; charset=utf-8'}
    url = f'https://rock.bytedance.net/api/v2/appealCaseList'
    params = {
        'verifier_type': 5,  # 0-初审/代操作，5-初判
        'case_state': 2,     # 0-待处理，2-已处理
        'search_value_enum': 0,
        'origin_audit_time': origin_audit_time,
        'order_field': 'open_time',
        'order': 1,
        'origin_verifier': origin_verifier,
        'start': 0,
        'end': 100,
    }
    r = requests.get(url=url, params=params, headers=header).text
    return json.loads(r)


# 获取ROCK数据-不分页-初审diff
def getRock_diff_list(cookie,start_time, end_time):
    page_index = 100    # 目前最大值，超过报错
    start_index = 0
    end_index = page_index
    result_list_1 = []
    url = f"https://rock.bytedance.net/api/v2/appealCaseList?verifier_type=0&case_state=0&search_value_enum=0&origin_audit_time={start_time}+00:00:00~{end_time}+23:59:59&order_field=remain_time&order=0&start={start_index}&end={end_index}"
    header = {"cookie": cookie, 'content-type': 'text/plain; charset=utf-8'}
    r = requests.get(url, headers=header)
    result = json.loads(r.text)
    all_count = 0
    all_count = result.get("data").get("count")
    result_list_1 = result.get("data").get("item_list")

    if all_count > page_index:
        length = all_count // page_index
        for i in range(1, length + 1):
            start_index = page_index * i + 1
            end_index = (i + 1) * page_index
            url = f"https://rock.bytedance.net/api/v2/appealCaseList?verifier_type=0&case_state=0&search_value_enum=0&origin_audit_time={start_time}+00:00:00~{end_time}+23:59:59&order_field=remain_time&order=0&start={start_index}&end={end_index}"
            r = requests.get(url, headers=header)
            result = json.loads(r.text)
            for item in result.get("data").get("item_list"):
                result_list_1.append(item)
    return result_list_1


# 获取ROCK数据-不分页-初审已申诉-case最终打标结果
def getRock_dealed_list(cookie,start_time, end_time):
    page_index = 100    # 目前最大值，超过报错
    start_index = 0
    end_index = page_index
    result_list_1 = []
    url = f"https://rock.bytedance.net/api/v2/appealCaseList?verifier_type=0&case_state=2&search_value_enum=0&origin_audit_time={start_time}+00:00:00~{end_time}+23:59:59&order_field=open_time&order=1&start={start_index}&end={end_index}"
    header = {"cookie": cookie, 'content-type': 'text/plain; charset=utf-8'}
    r = requests.get(url, headers=header)
    result = json.loads(r.text)
    all_count = 0
    all_count = result.get("data").get("count")
    result_list_1 = result.get("data").get("item_list")

    if all_count > page_index:
        length = all_count // page_index
        for i in range(1, length + 1):
            start_index = page_index * i + 1
            end_index = (i + 1) * page_index
            url = f"https://rock.bytedance.net/api/v2/appealCaseList?verifier_type=0&case_state=2&search_value_enum=0&origin_audit_time={start_time}+00:00:00~{end_time}+23:59:59&order_field=open_time&order=1&start={start_index}&end={end_index}"
            r = requests.get(url, headers=header)
            result = json.loads(r.text)
            for item in result.get("data").get("item_list"):
                result_list_1.append(item)

    return result_list_1
