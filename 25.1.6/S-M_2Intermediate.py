import re
import json

# # 定义提取函数
# def extract_action(response):
#     # 提取所有 Action
#     action_matches = re.findall(r"Action:\s*(\S.+?)\s*(?=\n|Action Input:|$)", response, re.DOTALL)
#     return action_matches
#
# def extract_input(response):
#     # 提取所有 Action Input
#     input_matches = re.findall(r"Action Input:\s*(\{.*?\})", response, re.DOTALL)
#     return input_matches

def extract_action_and_input(response):
    action_matches = re.findall(r"Action:\s*(\S.+?)\s*(?=\n|Action Input:|$)", response, re.DOTALL)
    input_matches = re.findall(r"Action Input:\s*(\{.*?\})", response, re.DOTALL)
    return list(zip(action_matches, input_matches))


# 读取 JSONL 文件并提取信息
def process_jsonl(file_path, filename):
    with open(f'{filename}_Intermediate.txt', 'w', encoding='utf-8') as f:
        with open(file_path, 'r', encoding='utf-8') as file:
            list_of_actions = []
            for line in file:
                data = json.loads(line.strip())  # 解析每一行的 JSON
                response = data.get('response', '')
                actions = extract_action_and_input(response)
                if actions:
                    for (action, action_input) in actions:
                        if action not in list_of_actions:
                            list_of_actions.append(action)
                            # f.write(f"ID: {data['id']} | Action: {action}\nID: {data['id']} | Input: {action_input}\n")
                            f.write(f"Action: {action}\nInput: {action_input}\n")

filelist = {'S-M'}
for file in filelist:
    # 调用函数并传入 JSONL 文件路径
    file_path = f'MTU-Bench/MTU-Eval/responses/{file}_gpt4_response.jsonl'
    process_jsonl(file_path, file)