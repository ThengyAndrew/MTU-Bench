import json
import re
import ast
import os
from idlelib.colorizer import matched_named_groups

Version = 1.0


if __name__ == '__main__':
    with open(f'eval.json','r', encoding="utf-8") as eval_file:
        eval_data = json.load(eval_file)
    with open(f"response_invalid.json","r",encoding="utf-8") as wrong_list_file:
        wrong_list = json.load(wrong_list_file)

    to_dump = []
    for eval in eval_data:
        id = eval['id']
        matched = re.match(f"MTU_Bench_S-S_(.+)", id)
        id_number = matched.group(1)
        if id_number not in wrong_list:
            to_dump.append(eval)
        else:
            print(f"{id_number} deleted!")

    with open(f"eval_new.json","w",encoding="utf-8") as eval_file:
        json.dump(to_dump,eval_file, ensure_ascii=False, indent=4)

    with open(f"eval_new.json","r",encoding="utf-8") as eval_file:
        new_data = json.load(eval_file)
        print(len(new_data))

