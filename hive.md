1、提取 未解析 的文本内容
> 如"[\"or\", [\"and\", [0, \"{originality_label}\", \"b1\"]]]"，
> "[\"or\", [\"and\", [0, \"{originality_label}\", \"a1\"]]]"，
> "[\"or\", [\"and\", [0, \"{originality_label}\", \"original\"]]]"，提取a1,b1,original，注意有两个original，我们需要的是单独存在的那个，
> 在用正则提取前，需要将\剔除掉


```
> 备注：目标存放至verify_rule字段中
select
    regexp_replace(verify_rule,'\\\\','') , # 在用正则提取前，需要将\剔除掉，否则第二个original会提取失败，原因可能是因为反斜杠导致的字符含义发生了变化，这里是四个\，没理解按道理2个就可以了
    regexp_extract(regexp_replace(verify_rule,'\\\\',''),'(a\\d|b\\d|c\\d|original)\"', 1)  # a1,b4,c2,d3,original
```

2、自定义排序
```
select
    task_id,
    verifier,
    sample_index,
    verify_data_map['originality_label'] AS `最后轮次`,
    row_number() over(
        PARTITION BY task_id
        ORDER BY CASE sample_index
        WHEN -2 THEN 1
        WHEN 2 THEN 2
        WHEN 1 THEN 3
        WHEN 0 THEN 4
        ELSE 5 
        END
    ) AS rank1
from
    tnscdm.dwd_tcs_task_verify_di
where
    date between '2023-12-01' and '${date-1}'
    and project_id in (1234567890)
    and is_resolve = 1
```
