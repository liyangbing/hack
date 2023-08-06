from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Route to serve static files from the 'static' directory
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@socketio.on('chatMessage')
def handle_message(message):
    print('Received message: ', message)
    emit('chatMessage',  message, broadcast=True)

@socketio.on('gptMessage')
def handle_message(message):
    print('Received message: ', message)
    emit('gptMessage',  message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=3000,debug=True)
