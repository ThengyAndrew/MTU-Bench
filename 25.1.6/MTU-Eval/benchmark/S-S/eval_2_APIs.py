import json
import re
import ast
import os

'''
come from `eval_processor2.py`, make jsonl to json.
'''

Version = 1.0
folder_path = f"APIs_Ver{Version}"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")


with open('S-S_eval.jsonl','r') as f:
    obj = []
    number = 0
    for line in f:
        with open(f'{folder_path}/APIs_{number}.json', 'w') as w:
            data = json.loads(line.strip())
            question = data['question']
            lines = question.splitlines()
            ptr = 0
            for line in lines:
                if ptr == 1:
                    if line != "":
                        extracted_text = line
                        break
                if line.startswith('The following is a list of APIs'):
                    ptr = 1
            candidate_apis = []
            converted_list = ast.literal_eval(extracted_text)
            # name = 0
            # while extracted_text[name:]:
            #     name = extracted_text[name:].find("name")
            #     pass
            json.dump(converted_list, w, indent=4, ensure_ascii=False)
            number+=1
print(number-1)