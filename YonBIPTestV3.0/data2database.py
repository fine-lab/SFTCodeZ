from util.docx_util import docx2list
from util.get_ids import get_sft_txt, get_id_10d
from pymongo import MongoClient


def docx2json(path):
    docx_list = docx2list(path)
    result = []
    input = ""
    output = ""
    for i in range(len(docx_list)):
        # count % 6 == 0, 获取question && output
        if i % 6 == 0:
            output = ""
            input = ""
            # 获取explain
            in_list = docx_list[i].split('--')
            if len(in_list) > 1:
                output = "根据"
            for j in range(1, len(in_list)):
                output += in_list[j]
            if len(in_list) > 1:
                output += "可知，"
            # 获取question
            # 获取answer
            if '（A）' in in_list[0]:
                output += '正确答案为: A'
                input = in_list[0].replace('（A）', ' ') + "：\n"
            elif '（B）' in in_list[0]:
                output += '正确答案为: B'
                input = in_list[0].replace('（B）', ' ') + "：\n"
            elif '（C）' in in_list[0]:
                output += '正确答案为: C'
                input = in_list[0].replace('（C）', ' ') + "：\n"
            elif '（D）' in in_list[0]:
                output += '正确答案为: D'
                input = in_list[0].replace('（D）', ' ') + "：\n"
        # i % 6 == 5, 添加数据
        elif i % 6 == 5:
            data = {}
            data["id"] = ""
            data["instruction"] = "请完成下述单选题。"
            data["input"] = input
            data["output"] = output
            data["system"] = ""
            data["history"] = []
            data["data_source"] = "蔡京生老师从领域获取的《YonBIP理念、价值和体系学习考试题库V3.0》"
            data["create_date"] = "2024-07-22"
            ids = get_id_10d(get_sft_txt(data, 's1'))
            data["id"] = ids
            result.append(data)
        # i % 6 == 1~4, 获取choices
        else:
            number = chr(ord('A') + i % 6 - 1)
            input = input + number + '. ' + docx_list[i] + '\n'
    return result


def json2database(data_list):
    client = MongoClient(host='10.0.50.5', port=27017,
                         username='yonyou',
                         password='youyon123')
    db = client["std"]
    col = db["std_sft_collect_YonBIP_exam_cn_s1"]
    insert_result = col.insert_many(data_list)
    # 输出插入的所有文档对应的 _id 值
    print(insert_result.inserted_ids)


path = r'D:\aData\SFT\sft数据整理0722\YonBIP理念、价值和体系学习考试题库V3.0.docx'
result = docx2json(path)
print(result)
json2database(result)
