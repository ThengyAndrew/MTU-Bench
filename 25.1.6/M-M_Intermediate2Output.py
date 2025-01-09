import json
import re


# 读取文件内容
def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# 处理每一行并生成所需的输出格式
def process_data(input_data):
    lines = input_data.strip().split("\n")
    result = []
    current_action = None
    current_id = None

    for line in lines:
        # 匹配 Action 行
        action_match = re.match(r"ID: (M-M_\d+_\d+) \| Action: (.+)", line)
        if action_match:
            # 如果是 Action 行，保存 Action 和 ID
            current_action = action_match.group(2)
            current_id = action_match.group(1)
            continue

        # 匹配 Input 行
        input_match = re.match(r"ID: (M-M_\d+_\d+) \| Input: (.+)", line)
        if input_match:
            # 如果是 Input 行，保存 Input 数据
            if current_action and input_match.group(1) == current_id:
                input_data = input_match.group(2)
                # 将 Input 解析为字典
                try:
                    arguments = json.loads(input_data)
                    # 构建目标格式
                    result.append({
                        "name": current_action,
                        "arguments": arguments
                    })
                except json.JSONDecodeError:
                    # 如果解析失败，跳过
                    pass
            continue

    return result


# 将结果写入 JSON 文件
def write_output_to_file(output_data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, indent=4, ensure_ascii=False)


# 主程序
def main(input_file_path, output_file_path):
    # 从文件读取输入数据
    input_data = read_input_file(input_file_path)

    # 处理数据
    formatted_data = process_data(input_data)

    # 将结果写入 JSON 文件
    write_output_to_file(formatted_data, output_file_path)
    print(f"数据已写入到 {output_file_path} 文件中。")

filelist = {'M-M'}
for file in filelist:
    input_file_path = f'{file}_Intermediate.txt'
    output_file_path = f'{file}_Output.json'
    main(input_file_path, output_file_path)

