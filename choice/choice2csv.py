import json
import re
import csv
from random import sample
from util.json_util import read_jsonl


def read_file(input_file):
    # 正则表达式模式，匹配问题和选项
    pattern = re.compile(r'^(.*?)A\.\s*(.*?)B\.\s*(.*?)C\.\s*(.*?)D\.\s*(.*)$', re.DOTALL)
    data = []
    bad_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            answer = item.get('output')
            instruction = item.get('instruction', '')
            match = pattern.match(instruction)
            # if match and item.get('score') > 0.8 and (answer in ['A', 'B', 'C', 'D'] or
            #     any(True if word in answer else False for word in ['A.', 'B.', 'C.', 'D.'])):
            question = match.group(1).strip()
            option_a = match.group(2).strip()
            option_b = match.group(3).strip()
            option_c = match.group(4).strip()
            option_d = match.group(5).strip()
            if match and item.get('score') > 0.8 and (answer in ['A', 'B', 'C', 'D'] or
                                                      any(True if word in answer else False for word in
                                                          ['A.', 'B.', 'C.', 'D.'])):
                data.append({
                    'id': item.get('id'),
                    'question': question,
                    'A': option_a,
                    'B': option_b,
                    'C': option_c,
                    'D': option_d,
                    'answer': answer,
                    'explanation': item.get('explain'),
                    'source': 'YonGPT',
                    # 'score': item.get('score'),
                    # 'score_dict': item.get('score_dict')
                })
            else:
                bad_data.append({
                    'id': item.get('id'),
                    'question': question,
                    'A': option_a,
                    'B': option_b,
                    'C': option_c,
                    'D': option_d,
                    'answer': answer,
                    'explanation': item.get('explain'),
                    'source': 'YonGPT',
                    'score': item.get('score'),
                    'score_dict': item.get('score_dict')
                })

    return data, bad_data


def write_data(data, output_file):
    # 写入 CSV 文件
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'question', 'A', 'B', 'C', 'D', 'answer', 'explanation', 'source'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f'Data has been successfully written to {output_file}')


def write_data_by_id(data, text_id_list, output_path):
    data_val_by_id = {}
    data_dev_by_id = {}
    data_by_id = {}
    for i in data:
        text_id = text_id_list[i['id']]
        if text_id in data_by_id:
            data_by_id[text_id].append(i)
        else:
            data_by_id[text_id] = [i]
    for i in data_by_id:
        n = len(data_by_id[i])
        sample_list = []
        if n <= 3:
            continue
        elif n < 20:
            sample_list = sample(data_by_id[i], 3)
        else:
            sample_list = sample(data_by_id[i], 5)
        data_dev_by_id[i] = sample_list
        data_val_by_id[i] = [j for j in data_by_id[i] if j not in data_dev_by_id[i]]

    # 写入val
    for i in data_val_by_id:
        f = output_path + r'\iKM_val\\' + str(i) + '.csv'
        write_data(data_val_by_id[i], f)
    # 写入dev
    for i in data_dev_by_id:
        f = output_path + r'\iKM_dev\\' + str(i) + '.csv'
        write_data(data_dev_by_id[i], f)

    # return data_val_by_id


def write_bad_data(bad_data, output_file):
    # 写入 CSV 文件
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'question', 'A', 'B', 'C', 'D', 'answer', 'explanation', 'source', 'score', 'score_dict'])
        writer.writeheader()
        for row in bad_data:
            writer.writerow(row)

    print(f'Data has been successfully written to {output_file}')


def get_text_id(choice_list):
    text_id_list = {}
    for l in choice_list:
        text_id_list[l.get('id')] = l.get('text_id')
    return text_id_list


if __name__ == '__main__':
    # 打开 JSONL 文件并读取内容
    input_file = r'D:\aData\SFT\0805extract选择题\0812v4_cut5000_1v5\0812iKM_choice_score_without_text_id.jsonl'
    choice_file = r'D:\aData\SFT\0805extract选择题\0812v4_cut5000_1v5\0812iKM_choice.jsonl'
    output_path = r'D:\aData\SFT\0805extract选择题\0812v4_cut5000_1v5'

    content = read_jsonl(choice_file)
    text_id_list = get_text_id(content)
    data, bad_data = read_file(input_file)
    write_data_by_id(data, text_id_list, output_path)