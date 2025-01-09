import json
import re

with open('M-M_eval.jsonl','r') as f:
    with open('M-M_eval_processed.json','w') as w:
        obj = []
        for line in f:
            data = json.loads(line.strip())
            answer = data['answer']
            # for name in answer:
            #     arguments = answer[name]
            # if answer:
            #     obj.append(answer)
            for name in answer:
                processed = {
                    'name': name,
                    'arguments': answer[name],
                }
                obj.append(processed)
        json.dump(obj, w, indent=4, ensure_ascii=False)
