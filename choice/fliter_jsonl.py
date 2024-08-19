import json
import re
import csv

# 打开 JSONL 文件并读取内容
input_file = r'D:\aData\SFT\0731SFTAuto\SFTAuto_v0731\data\translate\SID_FinGPT_FinGPT_en_s1.jsonl'
output_path = r'D:\aData\SFT\0731SFTAuto\SFTAuto_v0731\data\translate\SID_FinGPT_FinGPT_en_s1'

num = 50000
total = 378720
with open(input_file, 'r', encoding='utf-8') as f:
    i = 0
    data = []
    for line in f:
        item = json.loads(line)
        data.append(item)
        if i % num == num - 1 or i == total:
            # 写入 jsonl 文件
            file = output_path + r"\\" + str(i // num) + ".jsonl"
            with open(file, 'w', encoding='utf-8') as fw:
                for json_str in data:
                    fw.write(json.dumps(json_str, ensure_ascii=False) + '\n')

            print(f'Data has been successfully written to {file}')
            data = []
        i += 1
