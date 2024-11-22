# -- coding: utf-8 --**
import json

import requests
import os
from datetime import datetime

os.environ['CURL_CA_BUNDLE'] = ''

url = 'https://api.coze.cn/v3/chat'
headers = {
    "Authorization": "Bearer pat_gbdmxAxw2Asbp3BWpNyo4jZpYivBnCLz3BpIrM4iMbLdj7TY2fUD2YelxMuDqzsN",
    "Content-Type": "application/json",
    # "Accept": "*/*",
    # "Host": "api.coze.com",
    # "Connection": "keep-alive"
}

data = {
    "bot_id": "7427057791657443378",
    "user_id": "1112",
    "stream": True,
    "auto_save_history": False
}


def chat(query, history, user_id):
    chat_history = []
    for hist_item in history:
        chat_history.append({'role': 'user', 'type': 'question', 'content': hist_item[0], "content_type": "text"})
        chat_history.append({'role': 'assistant', 'type': 'answer', 'content': hist_item[1], "content_type": "text"})

    del chat_history[-1]
    del chat_history[-1]
    chat_history.append({'role': 'user', 'content': query, 'type': 'question', "content_type": "text"})

    print("用户说:", chat_history)
    if len(chat_history) > 10:
        data['additional_messages'] = chat_history[-10:]
    else:
        data['additional_messages'] = chat_history
    data['user_id'] = user_id
    # data['additional_messages']=data['additional_messages'].encode('utf-8')
    # data['chat_history'] = chat_history

    data_json = json.dumps(data)
    print(data_json)

    response = requests.post(url, headers=headers, data=data_json, stream=True)

    conti = False
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            if conti:
                conti = False
                continue
            event = extract_event_type(decoded_line)
            if event is not None and event == "[DONE]":
                break

            if event == "conversation.message.completed":
                conti = True
                continue

            if event is None:
                json_data = json.loads(decoded_line.split("data:")[-1])
                if 'type' in json_data and json_data['type'] == 'answer':
                    yield json_data['content']


def extract_event_type(event_str):
    # 判断字符串是否以"event:"开头
    if event_str.startswith("event:"):
        # 使用split()方法以":"分割字符串，并取分割后的第二个元素
        event_type = event_str.split(":", 1)[1]
        return event_type
    else:
        return None  # 如果不以"event:"开头，则返回None或你想要的任何默认值
