import random
from flask import Flask, request
from werkzeug.wrappers import Response
import json
import sys
sys.path.append("../")
from conversation.simple_completion import ask

# 定义数组
array = ["welcome", "chuckle", "thinking", "thinking2", "crossarm", "showing", "thanks", "thumbsup", "talk"]

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
    if type == 'text':
        result = ask(prompt)
    if type == 'audio':
        pass

    idx, val = get_random_element_and_index(array)
    data = {
        'type':type,
        'motionIndex': idx,
        'motionDesc': val,
        'data': result
    }
    response = Response(json.dumps(data), mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50002)
