import json
import re
import ast
import os

Version = 3.1
Upper_limit = 265

file_num = 0

query_folder_path = f"eval_Ver2.2"
folder_path = f'eval_output_Ver{Version}'

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功。")
else:
    print(f"文件夹 {folder_path} 已存在。")


def construct_query():
    with open(f"{query_folder_path}/eval_processed{file_num}.json", "r") as f:
        to_return = json.load(f)
    return to_return


def construct_candidate_apis(f):
    objects = json.load(f)
    for obj in objects:
        if obj['name']=="GetWeather":
            continue
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
        parameters = {"type":"object", "properties":properties, "required":required}
        function ={
            'name': obj['name'],
            "description": obj['description'],
            "parameters": parameters,
        }
        candidate_api = {
            "type":"function",
            "function": function
        }
        candidate_apis.append(candidate_api)

while file_num <= Upper_limit:
    candidate_apis = []
    with open(f'eval/eval_processed{file_num}.json','r') as f:
        with open(f'{folder_path}/M-M_eval_processed{file_num}.json','w') as w:
            objects = json.load(f)
            for obj in objects:
                if obj['name']=="GetWeather":
                    continue
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
                parameters = {"type":"object", "properties":properties, "required":required}
                function ={
                    'name': obj['name'],
                    "description": obj['description'],
                    "parameters": parameters,
                }
                candidate_api = {
                    "type":"function",
                    "function": function
                }
                candidate_apis.append(candidate_api)
            query_data = construct_query()
            json_to_write = {"query":query_data,"candidate_apis":candidate_apis}
            json.dump(json_to_write, w, indent=4, ensure_ascii=False)
            print(f"{file_num} done")
    file_num += 1