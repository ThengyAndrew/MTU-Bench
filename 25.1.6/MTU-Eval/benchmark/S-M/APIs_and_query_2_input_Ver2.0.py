import json
import re
import ast
import os

Version = 2.0
Upper_limit = 93

OBJECT = f"S-M"

query_folder_path = f"query_Ver1.0"
folder_path = f'{OBJECT}_eval_output_Ver{Version}'

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")


def construct_query():
    with open(f"{query_folder_path}/eval_processed{file_num}.txt", "r", encoding="utf-8") as f:
        to_return = f.read()
    return to_return

def construct_properties_and_required(obj):
    properties = {}
    required = []
    for param in obj['required_parameters']:
        try:
            properties[param['name']] = {}
            if 'type' in param:
                properties[param['name']]['type'] = param['type']
            if 'description' in param:
                properties[param['name']]['description'] = param['description']
            required.append(param['name'])
        except:
            pass
    for param in obj['optional_parameters']:
        try:
            properties[param['name']] = {}
            if 'type' in param:
                properties[param['name']]['type'] = param['type']
            if 'description' in param:
                properties[param['name']]['description'] = param['description']
        except:
            pass
    return properties, required

def construct_parameters(obj):
    properties_data, required_data = construct_properties_and_required(obj)
    parameters = {
        "type": "object",
        "properties": properties_data,
        "required": required_data
    }
    return parameters

def construct_function(obj):
    parameters_data = construct_parameters(obj)
    function = {
        'name': obj['name'],
        "description": obj['description'],
        "parameters": parameters_data,
    }
    return function

def construct_candidate_apis():
    with open(f'APIs_Ver1.0/APIs_{file_num}.json','r') as f:
        objects = json.load(f)
        candidate_apis = []
        for obj in objects:
            function_data = construct_function(obj)
            candidate_api = {
                "type":"function",
                "function": function_data
            }
            candidate_apis.append(candidate_api)

    return candidate_apis




if __name__ == '__main__':

    file_num = 0
    while file_num <= Upper_limit:

        with open(f'{folder_path}/eval_processed{file_num}.json','w') as w:

            query_data = construct_query()
            candidate_apis_data = construct_candidate_apis()
            json_to_write = {
                "query":query_data,
                "candidate_apis":candidate_apis_data
            }
            json.dump(json_to_write, w, indent=4, ensure_ascii=False)
            print(f"{file_num} done")

        file_num += 1