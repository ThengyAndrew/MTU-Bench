import json
import re
import ast
import os

Version = 1.0
Upper_limit = 472

store_folder_path = f'.'

# 检查文件夹是否存在，不存在则创建
if not os.path.exists(store_folder_path):
    os.makedirs(store_folder_path)
    print(f"文件夹 {store_folder_path} 创建成功。")
else:
    print(f"文件夹 {store_folder_path} 已存在。")


if __name__ == '__main__':

    file_num = 0
    list = []
    wrong_list = []
    with open(f'{store_folder_path}/eval.json','w', encoding="utf-8") as w:
        with open(f'wrong_list.json','w', encoding="utf-8") as wrong:
            while file_num <= Upper_limit:
                try:
                    with open(f'eval_standard_Ver1.0/eval{file_num}.json','r', encoding="utf-8") as r:
                        data_list = json.load(r)
                        for data in data_list:
                            if data['response'][0]['name']:
                                list.append(data)
                            else:
                                wrong_list.append(file_num)
                        print(f"{file_num} done")
                except:
                    pass
                file_num += 1
            json.dump(wrong_list, wrong, ensure_ascii=False)
        json.dump(list, w, indent=4, ensure_ascii=False)
