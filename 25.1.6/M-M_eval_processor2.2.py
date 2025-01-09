import json
import re
import ast
import os


Version = 2.2

folder_path = f'eval_Ver{Version}'

HEAD = f"History Dialog: \n"
END = f", \"answer\""

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")


number = 0
while number <=265:
    with open(f'eval_Ver2.1/eval_processed{number}.txt','r') as f:
        with open(f'{folder_path}/eval_processed{number}.json', 'w', encoding='utf-8') as json_file:
            content = f.read()
            dialog_history = []
            lines = content.split("\n\n")
            for line in lines:
                # 只处理非空行
                if line.strip():
                    parts = line.split("\n")  # 根据换行符分割每一行（用户、助手、行动等）

                    # 提取角色和消息
                    role_message = {}
                    for part in parts:
                        if part.startswith("User:"):
                            role_message["User"] = part[len("User:"):].strip()
                        elif part.startswith("Assistant:"):
                            role_message["Assistant"] =  part[len("Assistant:"):].strip()
                        elif part.startswith("Action:"):
                            pass

                    dialog_history.append(role_message)

            json.dump(dialog_history, json_file, indent=4, ensure_ascii=False)

    number+=1

