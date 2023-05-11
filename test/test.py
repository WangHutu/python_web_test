from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, emit
import threading
import queue
import logging
import subprocess
import pty
import os

import sys
sys.path.append('../venv')
# import eventlet
# eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

ttyd_process = None
output_queue = queue.Queue()
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('my-response', "Connected")

@socketio.on('send-message')
def handle_terminal_message(message):
    print(message, 'message------>')
    # 处理从客户端接收到的消息
    print('-----------received message-----------: ' + message)
    # socketio.emit("message",{"Data":'4564564'})
    # ttyd_process.stdin.write((message + '\n').encode())
    # ttyd_process.stdin.flush()
    # 执行命令
    command = message.strip()  # 获取客户端发送的命令并去除前后空格
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # 将结果发送回客户端
    socketio.emit('my-response', result.stdout)
    

# 启动 ttyd 进程并与其进行通信
def start_ttyd():
    global ttyd_process, ttyd_pty

    # 使用 pty 模块创建一个伪终端
    ttyd_pty, ttyd_slave = pty.openpty()

    # 启动 ttyd 进程，并将伪终端连接到其 stdin
    ttyd_command = ['ttyd', '-p', '8080', 'bash']
    ttyd_process = subprocess.Popen(ttyd_command, stdin=ttyd_slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 关闭从伪终端到 ttyd 进程的文件描述符
    os.close(ttyd_slave)

    # 读取 ttyd 进程的输出
    while True:
        output = os.read(ttyd_pty, 1024).decode().strip()
        if not output:
            break
        socketio.emit('my-response', output)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    ttyd_process = None
    ttyd_pty = None
    # start_ttyd()

    socketio.run(app, port=4200)
