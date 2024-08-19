# 参考代码
import json
from util.json_util import write_jsonl


def process_jsonl(file_path):
    yonyoueval_subject_mapping = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            article_id = data['id']
            article_title = data['title']
            content_length = len(data['content'])

            yonyoueval_subject_mapping[article_id] = [
                article_id,  # 文章ID
                article_title,  # 文章title
                content_length  # 文章content的长度
            ]
    return yonyoueval_subject_mapping


# Example usage
input_file = r'D:\aData\SFT\0805extract选择题\iKM.jsonl'
output_file = r'D:\aData\SFT\0805extract选择题\iKM_map.jsonl'
result = process_jsonl(input_file)
write_jsonl(output_file, result)
print(result)