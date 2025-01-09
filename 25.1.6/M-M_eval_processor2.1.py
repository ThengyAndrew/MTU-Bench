import json
import re
import ast
import os


Version = 2.1

folder_path = f'eval_Ver{Version}'

HEAD = f"History Dialog: \n"
END = f", \"answer\""

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")

with open('M-M_eval.jsonl','r') as f:
    obj = []
    number = 0
    for line in f:
        with open(f'{folder_path}/eval_processed{number}.txt', 'w') as w:
            data = json.loads(line.strip())
            question = data['question']
            start = question.find(HEAD) + len(HEAD)
            # end = question.find(END)
            query = question[start:].strip()
            w.write(f"{query}")
            number+=1
