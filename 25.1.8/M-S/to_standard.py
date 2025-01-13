import json
import re
import ast
import os

Version = 1.0
Upper_limit = 472


response_folder_path = f"response"
query_and_apis_folder_path = f"query&candidate_apis"
store_folder_path = f'eval_standard_Ver{Version}'

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(store_folder_path):
    os.makedirs(store_folder_path)
    print(f"文件夹 {store_folder_path} 创建成功。")
else:
    print(f"文件夹 {store_folder_path} 已存在。")


def read_response():
    with open(f"{response_folder_path}/eval_processed{file_num}.json", "r") as f:
        to_return = json.load(f)
    return to_return


def read_query_and_apis():
    with open(f"{query_and_apis_folder_path}/eval_processed{file_num}.json", "r") as f:
        to_return = json.load(f)
    return to_return


if __name__ == '__main__':

    file_num = 0
    while file_num <= Upper_limit:

        with open(f'{store_folder_path}/eval{file_num}.json','w', encoding="utf-8") as w:

            json_to_write = read_query_and_apis()
            json_to_write['response'] = read_response()
            list_mark = [json_to_write]
            json.dump(list_mark, w, indent=4, ensure_ascii=False)
            print(f"{file_num} done")

        file_num += 1