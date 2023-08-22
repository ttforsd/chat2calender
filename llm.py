import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from pytz import timezone
import json
from time import sleep

# date_time = datetime.now().strftime("%A %d/%m/%Y %H:%M")
# print(date_time)

load_dotenv()
url = os.getenv('LLM_URL')

chat_url = f"{url}/v1/chat/completions"
models_url = f"{url}/v1/models"

r = requests.get(f"{url}/v1/models")
print(r)
print(r.text)

def get_time(HK=False):
    if HK == False: 
        return datetime.now().strftime("%A %d/%m/%Y %H:%M")
    tz = timezone('Hongkong')
    date_time = datetime.now(tz).strftime("%A %d/%m/%Y %H:%M")
    return date_time


prompt1 = "You are given text containing info about a event. Extract date of event, time of event, name of event. Output json and nothing else. Example 1: Input: basketball game at 12am on 1/1, 11pm on 2/1. meeting with boss at 9am on 13 November; Output:[{'Event_Date': '1/1', 'Event_Time': '00:00', 'Event_Name': 'Basketball game'}, {'Event_Date': '2/1', 'Event_Time': '23:00', 'Event_Name': 'Basketball game'}, {'Event_Date': '13/11', 'Event_Time': '09:00', 'Event_Name': 'Meeting with boss'}] \n Example 2: Input: Vet clinics 5/5; Output:[{'Event_Date': '5/5', 'Event_Time': '00:00', 'Event_Name': 'Vet clinics'}]"


def call_llm(prompts): 
    base_message = {"role": "user"}
    messages = []
    date_time = get_time()
    date_time = f"Time now is {date_time}"
    system_message = {"content": date_time, "role": "system"}
    messages.append(system_message)
    for prompt in prompts:
        holder = base_message.copy()
        holder["content"] = prompt
        messages.append(holder)

    data = {
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.1,
    }
    print(data)
    r = requests.post(chat_url, json=data)
    print(f"Raw output: {r.text}")
    return r.json()

def text2json(text): 
    print(text)
    prompts = [prompt1]
    prompts.append(text)
    cal_json = call_llm(prompts)
    cal_json = cal_json['choices'][0]['message']['content']
    cal_json = extracter(cal_json)
    cal_json = json.loads(cal_json)
    if type(cal_json) != list: 
        cal_json = [cal_json]
    print(cal_json)
    return cal_json


def extracter(s): 
    pattern = "[{"
    for i in range(len(s) -1):
        if s[i:i+2] == pattern: 
            s = s[i:]
            break 
    s = s.replace("'", '"')
    return s

        
def long_wait(a):
     print("running")
     sleep(50)
     return a


# print(call_llm(["Where is the capital of France?"]))
