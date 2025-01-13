import json

def metrics(golden_answer, output_answer):
    '''
    在多轮单工具的前提下计算 APIAcc 和 APIParamAcc 两个指标。
    APIParamAcc是基于APIAcc的基础之上的。只对于相同的API进行Param比较

    Args:
        golden_answer (list): 黄金答案列表，每个元素是一个包含 `name` 和 `arguments` 的 dict。
        output_answer (list): 模型输出的答案列表，每个元素是一个包含 `name` 和 `arguments` 的 dict。

    Returns:
        dict: 包含 APIAcc 和 APIParamAcc 的结果。
    '''
    '''
    golden_answer =
    [
        {
            'arguments': {'area': 'Vacaville', 'furnished': 'True', 'number_of_beds': 3, 'pets_allowed': 'True'},
            'name': 'aaa'
        }
    ]
    '''
    # TODO: 如果 output 调用了多工具呢？
    total = len(golden_answer)
    total_params = 0
    matched_params = 0
    api_name_matches = 0
    # 经检查， eval 中所有 response 均为单工具调用
    gold = golden_answer[0]
    api_param_acc = 0.0
    for output in output_answer:
        if gold['name'] == output['name']:
            api_name_matches += 1
            gold_args = gold.get("arguments", {})
            output_args = output.get("arguments", {})
            for key, gold_value in gold_args.items():
                total_params += 1
                if key in output_args and output_args[key] == gold_value:
                    matched_params += 1
            api_param_acc = matched_params / total_params
    api_acc = api_name_matches / total
    return {"APIAcc": api_acc, "APIParamAcc": api_param_acc}

if __name__ == "__main__":
    golden_answer = [
        {
            'arguments': {
                'people': '6',
                'return_info': [
                    'reference'
                ],
                'trainID': 'TR9781'
            },
            'name': 'BookTrain'
        }
    ]

    # # {'APIAcc': 1.0, 'APIParamAcc': 1.0}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'BookTrain'
    #     }
    # ]

    # # {'APIAcc': 0.0, 'APIParamAcc': 0.0}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'Book'
    #     }
    # ]

    # # {'APIAcc': 1.0, 'APIParamAcc': 0.6666666666666666}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'wrong_answer'
    #         },
    #         'name': 'BookTrain'
    #     }
    # ]

    # # {'APIAcc': 1.0, 'APIParamAcc': 0.6666666666666666}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference', 'wrong_answer'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'BookTrain'
    #     }
    # ]

    # {'APIAcc': 2.0, 'APIParamAcc': 1.0}
    # 崩了
    # output_answer = [
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'BookTrain'
    #     },
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'BookTrain'
    #     }
    # ]

    # # {'APIAcc': 1.0, 'APIParamAcc': 1.0}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'BookTrain'
    #     },
    #     {
    #         'arguments': {
    #             'people': '6',
    #             'return_info': [
    #                 'reference'
    #             ],
    #             'trainID': 'TR9781'
    #         },
    #         'name': 'WRONG_ANSWER'
    #     }
    # ]

    # {'APIAcc': 2.0, 'APIParamAcc': 0.5}
    # 崩了
    output_answer = [
        {
            'arguments': {
                'people': '6',
                'return_info': [
                    'reference'
                ],
                'trainID': 'TR9781'
            },
            'name': 'BookTrain'
        },
        {
            'arguments': {
                'people': 'wrong_answer',
                'return_info': [
                    'wrong_answer'
                ],
                'trainID': 'wrong_answer'
            },
            'name': 'BookTrain'
        }
    ]

    # 测试函数
    result = metrics(golden_answer, output_answer)
    print(result)
