# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request,render_template
from flask_cors import CORS
from werkzeug.wrappers import Response 
import json
import json
from config.config import *
from conversation.chat_gpt import ChatSimpleGPT
from baby.picture import Pic

app = Flask(__name__)
CORS(app)  # 默认允许所有跨域请求

pic_server = Pic()


@app.route('/')
def home():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    response = Response(json.dumps(data), mimetype='application/json')
    return response

@app.route('/pic')
def pic_html():
    return render_template('pic.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    logging.info("recevie chat data: %s", data)
    text = data['prompt']
    response = pic_server.pic(text)
    # jsonify将Python对象转换为JSON格式
    logging.info("chat response: %s", response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=50002, debug=True)

