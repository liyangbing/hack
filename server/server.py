from flask import Flask, request
from werkzeug.wrappers import Response
import json
from conversation.langchain_agent import Assistant, langchain_agent

app = Flask(__name__)

assistant = Assistant()


@app.route('/')
def home():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    response = Response(json.dumps(data), mimetype='application/json')
    return response


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    question = request.form.get('question')
    assistant.ask(question)

    print(question)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
