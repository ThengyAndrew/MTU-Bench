import json
import re
import ast
import os

Version = 1.0


if __name__ == '__main__':
    # with open(f'check_output.txt','w', encoding="utf-8") as w:
    with open(f'eval.json','r', encoding="utf-8") as r:
        data_list = json.load(r)
        try:
            for data in data_list:
                if len(data['response'])!=1:
                    raise Exception("多工具调用")
        except Exception as e:
            print(e)
