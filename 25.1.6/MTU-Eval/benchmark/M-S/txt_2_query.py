import json
import os
import re

Version = 2.0

folder_path = f'query_Ver{Version}'

HEAD = f"History Dialog: \n"
END = f", \"answer\""

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")


number = 0
while number <=472:
    with open(f'query_Ver1.0/eval_processed{number}.txt','r', encoding='utf-8') as f:
        with open(f'{folder_path}/eval_processed{number}.json', 'w', encoding='utf-8') as json_file:
            content = f.read()
            dialog_history = []
            lines = content.split("\n\n")
            for line in lines:
                # 只处理非空行
                if line.strip():
                    parts = line.split("\n")  # 根据换行符分割每一行（用户、助手、行动等）

                    # 提取角色和消息

                    for part in parts:
                        if part.startswith("user:") or part.startswith("User:"):
                            role_message = {}
                            role_message["user"] = part[len("user:"):].strip()
                        elif part.startswith("assistant:"):
                            role_message["assistant"] =  part[len("assistant:"):].strip()
                            dialog_history.append(role_message)
                        else:
                            name = re.match(f'([^:]+):(.+)', part)
                            print(name.group(1))
                            print(name.group(2))
                            role_message[name.group(1)] = name.group(2)[1:]

            json.dump(dialog_history, json_file, indent=4, ensure_ascii=False)

    number+=1

