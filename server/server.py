# -*- coding: utf-8 -*-

import random
from flask import Flask, request
from werkzeug.wrappers import Response
import json
import sys
import requests
import json
import re
import requests
import os
import random
import string
from requests_toolbelt.multipart.encoder import MultipartEncoder
from flask_cors import CORS
CORS(app)  # 默认允许所有跨域请求

sys.path.append("../")
from conversation.chat_chatglm import ask
import base64

# 定义数组
array = ["welcome", "chuckle", "thinking", "thinking2", "crossarm", "showing", "thanks", "thumbsup", "talk"]

audio_url = "http://127.0.0.1:4523/m1/2848880-0-default/test"

abs_path = "/Users/lyb/code/aitest/hack/audio/"
base = "http://39.98.94.86:50003"

# 定义函数来随机返回数组中的一个元素及其索引（索引从1开始）
def get_random_element_and_index(arr):
    index = random.randint(0, len(arr) - 1)
    return index + 1, arr[index]

app = Flask(__name__)


@app.route('/')
def home():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    response = Response(json.dumps(data), mimetype='application/json')
    return response


# API返回的格式：1,text，2，audio（base64编码的wav） 
# 3，motionIndex：回答对应动作的index（1，2，3，4，5，6，7，8，9）
# 4，motionDesc：回答对应的动作指令（welcome,chuckle,thinking,thinking2,crossarm,showing,thanks,thumbsup,talk)
@app.route('/chat', methods=['POST', 'GET'])
def chat():
    data = request.get_json()
    key = data.get('key')
    prompt = data.get('prompt')
    type = data.get('type')
    print(key, prompt, type)

    result = ""
    result = ask(prompt)
    if type == 'audio':
        param = {}
        param["text"] = result
        result = voice_vits(result)

    idx, val = get_random_element_and_index(array)
    data = {
        'type':type,
        'motionIndex': str(idx),
        'motionDesc': val,
        'data': result
    }
    response = Response(json.dumps(data), mimetype='application/json')
    return response

    
# 语音合成 voice vits
# 语音合成 voice vits
def voice_vits(text, id=133, format="wav", lang="auto", length=1, noise=0.667, noisew=0.8, max=50):
    fields = {
        "text": text,
        "id": str(id),
        "format": format,
        "lang": lang,
        "length": str(length),
        "noise": str(noise),
        "noisew": str(noisew),
        "max": str(max)
    }
    boundary = '----VoiceConversionFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice"

    res = requests.post(url=url, data=m, headers=headers)
    fname = re.findall("filename=(.+)", res.headers["Content-Disposition"])[0]
    path = f"{abs_path}/{fname}"

    with open(path, "wb") as f:
        f.write(res.content)
    print(path)

    with open(path, "rb") as wav_file:
        wav_data = wav_file.read()
        base64_data = base64.b64encode(wav_data)
    print(base64_data)
    return base64_data
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50002)
    voice_vits("你好，我是小智，很高兴认识你。")


