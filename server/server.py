# -*- coding: utf-8 -*-

import eventlet
eventlet.monkey_patch()

from werkzeug.wrappers import Response
from flask import Flask, request, render_template, send_from_directory
import base64
from speech.speech_whisper import SpeechWhisper
from speech.speech_azure import SpeechAzure
from speech.speech_vits import SpeechVits
from conversation.chat_gpt import ChatSimpleGPT
from conversation.chat_chatglm import ChatGLM6B
from config.config import *
from flask_cors import CORS
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import time
from flask_socketio import SocketIO, emit
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 定义数组
array = ["welcome", "chuckle", "thinking", "thinking2",
         "crossarm", "showing", "thanks", "thumbsup", "talk"]

# 定义函数来随机返回数组中的一个元素及其索引（索引从1开始）


def get_random_element_and_index(arr):
    index = random.randint(0, len(arr) - 1)
    return index + 1, arr[index]


app = Flask(__name__)
# CORS(app)  # 默认允许所有跨域请求
socketio = SocketIO(app, cors_allowed_origins="*",
                    transports=['polling', 'websocket'])


# 初始化ChatGLM
if chat_glm == CHAT_GLM_35:
    chat_glm_impl = ChatSimpleGPT()
if chat_glm == CHAT_GLM_6B:
    chat_glm_impl = ChatGLM6B()

# 初始化voice_gml
if voice_glm == VOICE_VITS:
    voice_glm_impl = SpeechVits()
if voice_glm == VOICE_AZURE:
    voice_glm_impl = SpeechAzure()

voice_glm_whisper = SpeechWhisper()


@app.route('/')
def home():
    return render_template('index.html')

# Route to serve static files from the 'static' directory
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

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

    if key != secret_key:
        return Response(json.dumps({'error': 'key error'}), mimetype='application/json')

     # 打印data的数据类型
    logger.debug("data key: %s, prompt: %s, data_type: %s",
                  key, prompt, data_type)

    # 如果是音频先转为文字
    is_from_audio = False
    from_audio_text = ""
    if data_type == "from_audio":
        audio_data = data.get('prompt')
        prompt = voice_glm_whisper.audio_2_text(audio_data)
        data_type = "audio"
        is_from_audio = True
        from_audio_text = prompt

    # 获取生成式内容

    answer = chat_glm_impl.ask(prompt)
    action_answer = chat_glm_impl.action(answer)

    logger.debug("result: %s, action %s", answer, action_answer)
    idx, val = get_random_element_and_index(array)
    for i in range(len(array)):
        if array[i] == action_answer:
            idx = i + 1
            val = action_answer
            break

    # 生成应答
    response_data = {
        'type': data_type,
        'motionIndex': str(idx),
        'motionDesc': val,
        'data': answer
    }

    if data_type == 'audio':
        audio_answer = voice_glm_impl.text_2_audio(answer)
        response_data['data'] = answer
        response_data['audio_data'] = audio_answer
        if is_from_audio:
            response_data['from_audio_data'] = from_audio_text

    response = Response(json.dumps(response_data), mimetype='application/json')
    end_time = time.time()
    logger.info("chat elase time: %s秒", end_time - start)
    return response


@app.route('/stream')
def index():
    return render_template('index_stream.html')

def send_message_callback(message):
    # Ensure message is in correct format
    if not isinstance(message, dict) or 'messageId' not in message or 'messageText' not in message or 'finished' not in message:
        logger.info('Error: Invalid message format %s', message)
        return

    # Convert dict to JSON and emit message
    message_json = json.dumps(message)
    logger.info("message_json: %s", message_json)
    socketio.emit('gptMessage', message)


@socketio.on('chatMessage')
def handle_message(data):
      # 开始时间
    start = time.time()
    logger.info("chatMessage handle_message: %s", data)
    socketio.emit('chatMessage', data)

    if not data:
        logger.info('Error: No data received')
        return
    # Parse JSON data
    try:
        # data不是dict类型，需要转换
        if data != None and not isinstance(data, dict):
            data_json = json.loads(data)
        else:
            data_json = data
    except json.JSONDecodeError:
        logger.error('Error: Invalid JSON data')
        return

    # Ensure data is in correct format
    if not isinstance(data_json, dict) or 'messageId' not in data_json or 'messageText' not in data_json or 'forceUpdate' not in data_json:
        logger.info('Error: Invalid data format')
        return

    if not data_json['messageText']:
        logger.info('Error: messageText is null')
        return

    # Pass data to chat stream function
    chat_glm_impl.chat_stream(data_json, send_message_callback)

    end_time = time.time()
    logger.info("chatMessage elase time: %s秒", end_time - start)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=50002, debug=True)
