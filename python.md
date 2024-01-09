# python-notepad
1. 将文本类型的list转为list
```
import json

str_list = "[11.23,23.34]"
list_list = json.loads(str_list)
print(type(list_list))

```
2. 用Pandas把数据生成到excel的时候如何避免科学记数法？
```
import pandas as pd
import json

# x.csv中有一列中每个单元格包含一个数组
df = pd.read_csv(r'C:\Users\Admin\Downloads\x.csv')
result = []
# 将每个文本类型的list转为list后，进行合并去重
for each in df['_col1']:
    each = json.loads(each)
    # print(type(each)
    result.extend(each)
result = list(set(result))
print(len(result))

data = {'ids':result}
df1 = pd.DataFrame(data)
df1['ids'] = df1['ids'].astype('str')  # 写入前将该列转为str，防止科学计数法
df1.to_excel(r'C:\Users\Admin\Downloads\yancong.xlsx',sheet_name='hah',index=False)

```
