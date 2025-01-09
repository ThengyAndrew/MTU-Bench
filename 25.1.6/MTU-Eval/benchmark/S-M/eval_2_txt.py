import json
import re
import ast
import os


Version = 1.0

folder_path = f'query_Ver{Version}'

HEAD = f"History Dialog: \n"
END = f", \"answer\""

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")

with open('S-M_eval.jsonl','r') as f:
    obj = []
    number = 0
    for line in f:
        with open(f'{folder_path}/eval_processed{number}.txt', 'w', encoding='utf-8') as w:
            data = json.loads(line.strip())
            question = data['question']
            lines = question.splitlines()
            ptr = 0
            for line in lines:
                if ptr == 1:
                    query = line[len("User: "):]
                    w.write(f"{query}")
                if line.startswith('The following is a list of APIs'):
                    ptr = 1
            # start = question.find(HEAD) + len(HEAD)
            # # end = question.find(END)
            # query = question[start:].strip()

            number+=1
