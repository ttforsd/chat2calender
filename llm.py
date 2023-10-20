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

def read_prompt(): 
    with open("prompt.txt", "r") as f:
        return f.read()




def call_llm(data): 
    print(data)
    print(data)
    r = requests.post(chat_url, json=data)
    print(f"Raw output: {r.text}")
    return r.json()

def text2request(text): 
    print(text)
    date_time = get_time()
    date_time = f"For your reference, date_time_now is {date_time}."
    text = f"{date_time} Prompt: {text}"
    print(text)
    prompt1 = read_prompt()
    prompt1 += text
    print(prompt1)
    # prompt1 to json format for llm 
    llm_request = {} 
    llm_request["messages"] = [{"role": "user", "content": prompt1}, {"role": "system", "content": "You ONLY return JSON, NOTHING ELSE"}]
    llm_request["max_tokens"] = 1024
    llm_request["temperature"] = 0.1
    print(llm_request)
    return llm_request


def text2json(text): 
    llm_request = text2request(text)
    cal_json = call_llm(llm_request)
    cal_json = cal_json['choices'][0]['message']['content']
    cal_json = extracter(cal_json)
    cal_json = json.loads(cal_json)
    if type(cal_json) != list: 
        cal_json = [cal_json]
    print(cal_json)
    return cal_json


def extracter(s): 
    s = s.replace("\n", "")
    pattern = "[{"
    for i in range(len(s) -1):
        if s[i:i+2] == pattern: 
            s = s[i:]
            break 
    s = s.replace("'", '"')
    s = s.replace("},]", "}]")
    return s

        
def long_wait(a):
     print("running")
     sleep(50)
     return a


# print(call_llm(["Where is the capital of France?"]))
