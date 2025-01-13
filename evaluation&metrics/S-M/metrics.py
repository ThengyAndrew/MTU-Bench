import json

def metrics(golden_answer, output_answer):
    '''
    在单轮多工具的前提下计算 APIAcc 和 APIParamAcc 两个指标。
    APIParamAcc是基于APIAcc的基础之上的。只对于相同的API进行Param比较

    Args:
        golden_answer (list): 黄金答案列表，每个元素是一个包含 `name` 和 `arguments` 的 dict。
        output_answer (list): 模型输出的答案列表，每个元素是一个包含 `name` 和 `arguments` 的 dict。

    Returns:
        dict: 包含 APIAcc 和 APIParamAcc 的结果。
    '''
    # TODO: 考虑对同一工具的反复调用对 APIAcc 的影响
    total = len(golden_answer)
    total_params = 0
    matched_params = 0
    api_name_matches = 0
    for gold in golden_answer:
        outputs = [i for i in output_answer if i['name']==gold['name']]
        if outputs:
            api_name_matches += 1
            for output in outputs:
                gold_args = gold.get("arguments", {})
                output_args = output.get("arguments", {})
                for key, gold_value in gold_args.items():
                    total_params += 1
                    if key in output_args and output_args[key] == gold_value:
                        matched_params += 1
    api_acc = api_name_matches / total
    api_param_acc = matched_params / total_params
    return {"APIAcc": api_acc, "APIParamAcc": api_param_acc}

if __name__ == "__main__":
    golden_answer = [
        {
            'arguments': {
                'artist': 'Taylor Swift'
            },
            'name': 'LookupSong'
        },
        {
            'arguments': {
                'recurrence': ['today'],
                'sound': 'LookupSong.song_name',
                'time': '15:00'
            },
            'name': 'change_alarm_sound'
        },
        {
            'arguments': {
                'appointment_date': '2024-04-05',
                'appointment_time': '15:00',
                'dentist_name': 'Dr. Clarke'
            },
            'name': 'BookAppointment'
        },
        {
            'arguments': {
                'appointment_date': '2024-04-05',
                'appointment_name': 'Dentist appointment with Dr. Clarke',
                'appointment_time': '15:00',
                'reminder_time': '2 hours before'
            },
            'name': 'set_appointment_reminder'
        }
    ]

    # {'APIAcc': 1.0, 'APIParamAcc': 1.0}
    '''
    output_answer = [ 
        {
            'arguments': {
                'artist': 'Taylor Swift'
            },
            'name': 'LookupSong'
        },
        {
            'arguments': {
                'recurrence': ['today'],
                'sound': 'LookupSong.song_name',
                'time': '15:00'
            },
            'name': 'change_alarm_sound'
        },
        {
            'arguments': {
                'appointment_date': '2024-04-05',
                'appointment_time': '15:00',
                'dentist_name': 'Dr. Clarke'
            },
            'name': 'BookAppointment'
        },
        {
            'arguments': {
                'appointment_date': '2024-04-05',
                'appointment_name': 'Dentist appointment with Dr. Clarke',
                'appointment_time': '15:00',
                'reminder_time': '2 hours before'
            },
            'name': 'set_appointment_reminder'
        }
    ]
    '''

    # # {'APIAcc': 0.25, 'APIParamAcc': 1.0}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'artist': 'Taylor Swift'
    #         },
    #         'name': 'LookupSong'
    #     }
    # ]

    # # {'APIAcc': 0.75, 'APIParamAcc': 0.8888888888888888}
    # output_answer = [
    #     {
    #         'arguments': {
    #             'artist': 'Taylor Swift'
    #         },
    #         'name': 'LookupSong'
    #     },
    #     {
    #         'arguments': {
    #             'artist': 'Taylor'
    #         },
    #         'name': 'LookupSong'
    #     },
    #     {
    #         'arguments': {
    #             'appointment_date': '2024-04-05',
    #             'appointment_time': '15:00',
    #             'dentist_name': 'Dr. Clarke'
    #         },
    #         'name': 'BookAppointment'
    #     },
    #     {
    #         'arguments': {
    #             'appointment_date': '2024-04-05',
    #             'appointment_name': 'Dentist appointment with Dr. Clarke',
    #             'appointment_time': '15:00',
    #             'reminder_time': '2 hours before'
    #         },
    #         'name': 'set_appointment_reminder'
    #     }
    # ]


    # {'APIAcc': 1.0, 'APIParamAcc': 0.5}
    # 实际上少调了一次 API，但是对 APIAcc 完全没有影响
    # golden_answer = [
    #     {
    #         'arguments': {
    #             'artist': 'Taylor Swift'
    #         },
    #         'name': 'LookupSong'
    #     },
    #     {
    #         'arguments': {
    #             'artist': 'Taylor'
    #         },
    #         'name': 'LookupSong'
    #     }
    # ]
    # output_answer = [
    #     {
    #         'arguments': {
    #             'artist': 'Taylor Swift'
    #         },
    #         'name': 'LookupSong'
    #     }
    # ]

    # 测试函数
    result = metrics(golden_answer, output_answer)
    print(result)
