import json
import re
import ast

Upper_limit = 265

file_num = 0

while file_num <= Upper_limit:
    candidate_apis = []
    with open(f'eval/eval_processed{file_num}.json','r') as f:
        with open(f'eval_output/M-M_eval_processed{file_num}.json','w') as w:
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
            json_to_write = {"candidate_apis":candidate_apis}
            json.dump(json_to_write, w, indent=4, ensure_ascii=False)
            print(f"{file_num} done")
    file_num += 1