from flask import Flask, request
from werkzeug.wrappers import Response
import json
import sys
sys.path.append("../")
from conversation.simple_completion import ask

app = Flask(__name__)


@app.route('/')
def home():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    response = Response(json.dumps(data), mimetype='application/json')
    return response


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

    data = {
        'type':type,
        'data': result
    }
    response = Response(json.dumps(data), mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50002)
