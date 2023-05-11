from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, emit

import sys
sys.path.append('../venv')
# from flask_cors import CORS
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# CORS(app, resources=r'/*')
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('my-response', {'data': {'data':'Connected'}})

@socketio.on('send-message')
def handle_terminal_message(message):
    print(message, 'message------>')
    emit('my-response', {'data': message})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, port=4200)
