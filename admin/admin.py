from flask import Flask, request, jsonify

app = Flask(__name__)

data = [{"question": "Question 1", "answer": "Answer 1"},
        {"question": "Question 2", "answer": "Answer 2"}]

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    print(data)
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
