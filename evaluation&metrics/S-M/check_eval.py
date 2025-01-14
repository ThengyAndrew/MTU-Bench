import json
import re
import ast
import os

Version = 1.0


if __name__ == '__main__':
    with open(f'eval.json','r', encoding="utf-8") as r:
        with open(f"response_invalid.json", 'w', encoding="utf-8") as w:
            wrong_list = []
            data_list = json.load(r)
            num = 0
            wrong_num = 0
            for data in data_list:
                # try:
                response = data['response']
                apis_list = data['candidate_apis']
                for call in response:
                    matched_apis = [i for i in apis_list if i['function']['name'] == call['name'] ]
                    if len(matched_apis) == 0:
                        id = data['id']
                        matched_groups = re.search(f"MTU_Bench_S-M_(.+)", id)
                        wrong_list.append(matched_groups.group(1))
                        wrong_num += 1

                #             raise Exception(f"{data['id']}:无源 API")
                # except Exception as e:
                #     print(f"{e}")
                num+=1
            json.dump(wrong_list, w)
        print(f"{wrong_num}")