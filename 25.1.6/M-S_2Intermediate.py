import re
import json

# 定义提取函数
def extract_action(response):
    # 使用正则表达式查找 'Action:' 后的内容
    match = re.search(r'Action:\s*([^\n]+)\n', response) # Action: "get_current_temperature"
    if match:
        return match.group(1)  # 提取括号内的内容
    return None

def extract_input(response):
    match = re.search(r'Action Input:\s*(\{[^}]+})', response) # Action Input: {"location": "living room"}
    if match:
        return match.group(1)  # 提取括号内的内容
    return None

# 读取 JSONL 文件并提取信息
def process_jsonl(file_path, filename):
    with open(f'{filename}_Intermediate.txt', 'w', encoding='utf-8') as f:
        with open(file_path, 'r', encoding='utf-8') as file:
            actions = []
            inputs = []
            for line in file:
                data = json.loads(line.strip())  # 解析每一行的 JSON
                response = data.get('response', '')
                action = extract_action(response)
                if action:
                    f.write(f"ID: {data['id']} | Action: {action}\n")
                    actions.append(action)
                action_input = extract_input(response)
                if action_input:
                    f.write(f"ID: {data['id']} | Input: {action_input}\n")
                    inputs.append(action_input)

filelist = {'M-S'}
for file in filelist:
    # 调用函数并传入 JSONL 文件路径
    file_path = f'MTU-Bench/MTU-Eval/responses/{file}_gpt4_response.jsonl'
    process_jsonl(file_path, file)