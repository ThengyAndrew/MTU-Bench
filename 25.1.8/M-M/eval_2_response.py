import json
import re
import ast
import os


Version = 1.0

eval_folder_path = f'eval'
store_folder_path = f'response'

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(store_folder_path):
    os.makedirs(store_folder_path)
    print(f"文件夹 {store_folder_path} 创建成功。")
else:
    print(f"文件夹 {store_folder_path} 已存在。")

with open(f'{eval_folder_path}/M-M_eval.jsonl','r') as f:
    obj = []
    number = 0
    for line in f:
        with open(f'{store_folder_path}/eval_processed{number}.json', 'w') as w:
            data = json.loads(line.strip())
            answers= data['answer']
            calls = []
            for answer in answers:
                call = {}
                call['name'] = answer
                call['arguments'] = answers[answer]
                calls.append(call)
            json.dump(calls, w, ensure_ascii=False, indent=4)
            number+=1
