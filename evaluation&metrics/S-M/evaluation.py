from transformers import AutoTokenizer
from datasets import Dataset
import json
import os
# from vllm import LLM, SamplingParams
from metrics import metrics
import re
print("import finished!")


def read_data(data_path):# done
    '''
    读取json
    '''
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"文件 {data_path} 不存在。")
    file_extension = os.path.splitext(data_path)[-1].lower() # 扩展名
    if file_extension == ".json":
        try:
            with open(data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"读取 JSON 文件时发生错误: {e}")
    '''
    data = [{'candidate_apis': [{'function': {'description': 'Play specific tracks from a given artist for a specific time duration.', 'name': 'spotify.play', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}], 'query': 'Play songs from the artists Taylor Swift and Maroon 5, with a play time of 20 minutes and 15 minutes respectively, on Spotify.', 'response': [{'arguments': {'artist': 'Taylor Swift', 'duration': 20}, 'name': 'spotify.play'}, {'arguments': {'artist': 'Maroon 5', 'duration': 15}, 'name': 'spotify.play'}]}]

    data = [{'candidate_apis': [{'function': {'description': 'Retrieves the current availability status of a specific book, indicating whether it is in stock, checked out, or reserved.', 'name': 'get_book_status', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}, {'function': {'description': 'Allows a user to extend the borrowing period for books currently checked out, subject to library policies and availability.', 'name': 'renew_books', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}, {'function': {'description': 'Enables a user to place a reservation on a book that is currently loaned out, notifying the user when the book becomes available.', 'name': 'reserve_book', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}, {'function': {'description': 'Calculates any late fees accrued on a user’s account for books not returned by their due date, potentially offering breakdowns by book or date range.', 'name': 'get_late_fees', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}, {'function': {'description': 'Facilitates the process for users to apply for a new membership with the library or bookstore, which may include online forms and submission of required documents.', 'name': 'apply_for_membership', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}, {'function': {'description': 'Processes payments made by users for various services, including late fees, membership fees, or purchasing books, offering multiple payment methods.', 'name': 'make_payment', 'parameters': {'properties': {...}, 'required': [...], 'type': 'object'}}, 'type': 'function'}], 'query': [{'Assistant': 'Sure, how can I assist you with that?', 'User': 'Can you help me check something in the library?'}, {'Assistant': 'You have a late fee of 50 dollars.', 'User': 'I want to check if I have any late fees for the books I borrowed.'}, {'User': 'Alright. I would like to pay them off. Can I make the payment by Credit Card?'}], 'response': [{'arguments': {'account_number': '123456', 'payment_amount': 'get_late_fees.late_fees', 'payment_method': 'Credit Card'}, 'name': 'make_payment'}]}]    '''

class SystemPrompt:# don't know
    """
    根据不同的模式生成对应的 system_prompt。
    难度分类：单轮单工具，单轮单工具多次，单轮多工具无依赖性，单轮多工具有依赖
    """
    def __init__(self, mode):
        self.mode = mode

    def get_prompt(self):
        if self.mode == 'single_tool_with_once':
            return '''单轮单工具'''
        elif self.mode == 'more_tools_with_once':
            return '''单轮多工具'''
        else:
            return '''333'''

def evaluate_pipeline(data_path, model_path, tokenizer_path, mode):
    data_list = read_data(data_path)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    sampling_params = SamplingParams(
        max_tokens=8192,
        temperature=0.0
    )
    llm = LLM(
        model = model_path
    )
    for data in data_list:
        system_prompt = SystemPrompt(mode).get_prompt()
        messages = [
            {   "role": "user",
                "content": data.get("query"),
            }
        ]
        tools = data.get("candidate_apis")
        model_input = tokenizer.apply_chat_template(
            messages,
            tools=tools,
            tokenize=False,
            add_generation_prompt=True
        )
        print(model_input)
        outputs = llm.chat(
            messages = messages,
            sampling_params = sampling_params,
            tools = tools,
            add_generation_prompt=True,
        )
        output_answer = outputs[0].outputs[0].text.strip()
        print(output_answer)
        output_answer = extract(output_answer)
        golden_answer = data.get("response")
        '''
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
        '''
        print(f"type of golden_answer is {type(golden_answer)}")
        print(f"type of output_answer is {type(output_answer)}")
        ans = metrics(golden_answer=golden_answer, output_answer=output_answer)
        print(ans)

if __name__ == "__main__":
    model_path = "/home/jovyan/fdu_new/models/Qwen2.5-7B-Instruct"
    tokenizer_path = "/home/jovyan/fdu_new/models/Qwen2.5-7B-Instruct"
    data_path = "test.json"
    mode = "more_tools_with_once"
    evaluate_pipeline(data_path, model_path, tokenizer_path, mode)