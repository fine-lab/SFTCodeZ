import tablib
import pandas as pd
import json


def excel_to_listdict(df):
    header = list(df.columns)
    list_dic = []  # excel转list嵌套dict
    for i in df.values:  # i 为每一行的value的列表
        for j in range(len(i)):
            if (pd.isnull(i[j])):
                i[j] = ' '
        a_line = dict(zip(header, i))
        list_dic.append(a_line)
    return list_dic


def list_to_excel(file, header, result):
    data = []
    for row in result:
        body = []
        for i in row.values():
            body.append(i)
        data.append(tuple(body))
    data = tablib.Dataset(*data, headers=header)
    open(file, 'wb').write(data.xls)


def excel_to_json(path, filename):
    df = pd.read_excel(path + filename + '.xlsx')
    result = excel_to_listdict(df)
    with open(path + filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    f.close()


# excel_to_json('D:\\aData\\数据处理\\34\\', '50行示例')
