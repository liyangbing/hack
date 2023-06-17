# -*- coding: utf-8 -*-

import random
import time
from flask import Flask, request
from werkzeug.wrappers import Response
import json
import json
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder
from flask_cors import CORS
import whisper

from config.config import *

from conversation.chat_chatglm import ChatGLM6B
from conversation.simple_completion import ChatSimpleGPT
from speech.speech_vits import SpeechVits
from speech.speech_azure import SpeechAzure

import base64

# 定义数组
array = ["welcome", "chuckle", "thinking", "thinking2", "crossarm", "showing", "thanks", "thumbsup", "talk"]

# 定义函数来随机返回数组中的一个元素及其索引（索引从1开始）
def get_random_element_and_index(arr):
    index = random.randint(0, len(arr) - 1)
    return index + 1, arr[index]

app = Flask(__name__)
CORS(app)  # 默认允许所有跨域请求

# 初始化ChatGLM
if chat_glm == CHAT_GLM_35:
    chat_glm = ChatSimpleGPT()
if chat_glm == CHAT_GLM_6B:
    
    chat_glm = ChatGLM6B()

# 初始化voice_gml   
if voice_gml == VOICE_VITS:
    voice_gml = SpeechVits()
if voice_gml == VOICE_AZURE:
    voice_gml = SpeechAzure()


@app.route('/')
def home():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    response = Response(json.dumps(data), mimetype='application/json')
    return response

audio_model = whisper.load_model("small")

# API返回的格式：1,text，2，audio（base64编码的wav） 
# 3，motionIndex：回答对应动作的index（1，2，3，4，5，6，7，8，9）
# 4，motionDesc：回答对应的动作指令（welcome,chuckle,thinking,thinking2,crossarm,showing,thanks,thumbsup,talk)
@app.route('/chat', methods=['POST', 'GET'])
def chat():
    # 打印方法的消耗时间
    # 开始时间
    start = time.time()

    # print reqest，格式为json
    data = request.get_json()

    key = data.get('key')
    prompt = data.get('prompt')
    data_type = data.get('type')

     # 打印data的数据类型
    logging.debug("data key: %s, prompt: %s, data_type: %s", key, prompt, data_type)

    # 如果是音频先转为文字
    is_from_audio = False
    from_audio_text = ""
    if data_type == "from_audio":
        audio_data = data.get('prompt')
        decoded_audio = base64.b64decode(audio_data)
        
        # AUDIO_SAVA_PATH, 时间戳，生成文件名
        out_file = f"{AUDIO_SAVA_PATH}/{int(time.time())}.wav"
        with open(out_file, "wb") as f:
                f.write(decoded_audio)

        result = audio_model.transcribe(audio=out_file, initial_prompt="这里是黑客松直播间，你是虚拟数字人思思。")
        logging.debug("audio to text, out_file:  %s, result: %s,text: %s", out_file,  result, result["text"])

        prompt = result["text"]
        data_type = "audio"
        is_from_audio = True
        from_audio_text = prompt

    # 获取生成式内容
    
    answer = chat_glm.ask(prompt)
    action_answer = chat_glm.action(answer)
   
    logging.debug("result: %s, action %s", answer, action_answer)
    idx, val = get_random_element_and_index(array)
    for i in range(len(array)):
        if array[i] == action_answer:
            idx = i + 1
            val = action_answer
            break

    # 生成应答
    response_data = {
        'type':data_type,
        'motionIndex': str(idx),
        'motionDesc': val,
        'data': answer
    }

    if data_type == 'audio':
        audio_answer = voice_gml.text_2_audio(answer)
        response_data['data'] = answer
        response_data['audio_data'] = audio_answer
        if is_from_audio:
            response_data['from_audio_data'] = from_audio_text


    response = Response(json.dumps(response_data), mimetype='application/json')
    end_time = time.time()
    logging.debug("chat elase time: %s秒, input %s, output %s", end_time - start)
    return response

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50002)
