import os
import sys
import json
import ast

FROM_PATH = os.path.join(os.path.dirname(__file__), "downloaded", "MTU-Bench")
TO_PATH = os.path.join(os.path.dirname(__file__), "processed", "MTU-Bench")

File_list = ["S-S"]

def construct_candidate_tools(question):
    lines = question.splitlines()
    ptr = 0
    for line in lines:
        if ptr == 1:
            if line != "":
                extracted_text = line
                break
        if line.startswith('The following is a list of APIs'):
            ptr = 1
    init_tools = ast.literal_eval(extracted_text)
    '''
    context = [
        {   
            'description': 'Reserve a table at a restaurant', 
            'name': 'ReserveRestaurant', 
            'optional_parameters': {'date': '2019-03-01','party_size': '2'}, 
            'required_parameters': ['restaurant_name','city','time'], 
            'result_parameters': ['restaurant_name','date', 'time', 'serves_alcohol', 'has_live_music', 'phone_number', 'street_address', 'party_size', 'price_range', 'city', 'cuisine']
        },
        {
            'description': 'Find a restaurant of a particular cuisine in a city', 
            'name': 'FindRestaurants', 
            'optional_parameters': {'has_live_music': 'dontcare', 'price_range': 'dontcare', 'serves_alcohol': 'dontcare'}, 
            'required_parameters': ['cuisine', 'city'], 'result_parameters': ['restaurant_name', 'serves_alcohol', 'has_live_music', 'phone_number', 'street_address', 'price_range', 'city', 'cuisine']
        }
    ]
    '''
    candidate_tools = {
        "role": "candidate_tools",
        "context": context,
    }
    list_of_candidates = []
    return list_of_candidatesz

def process_s_s(from_path, to_path):
    print("S_S processed!")
    with open(os.path.join(from_path, "S-S_eval.jsonl")) as fin:
        for line in fin:
            id = json.loads(line)["id"]
            question = json.loads(line)["question"]
            answer = json.loads(line)["answer"]
            candidate_tools = construct_candidate_tools(question)




def processor():
    process_s_s(FROM_PATH, TO_PATH)
    print("MTU-Bench processed!")


if __name__ == "__main__":
    processor()