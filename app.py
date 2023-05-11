from flask import Flask, request, jsonify
import registerLogin
import boards
import admins
import logs
import power
import reimage
import tools
import subprocess
import sys
sys.path.append('./venv')
from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from flask_sockets import Sockets
# from subprocess import Popen, PIPE, STDOUT

app = tools.create_flask_app()
# CORS(app, cors_allowed_origins='*', credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', async_handlers=False)
 
# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    return registerLogin.login(request)
    


# 注册接口
@app.route('/register', methods=['POST'])
def register():
    return registerLogin.register(request)


# 开发板类型获取
@app.route('/getTypeList', methods=['GET'])
def getTypeList():
    return boards.getTypeList(request)


# 开发板类型增加
@app.route('/insertTypeList', methods=['POST'])
def insertTypeList():
    return boards.insertTypeList(request)


# 开发板类型更新
@app.route('/updateTypeList', methods=['POST'])
def updateTypeList():
    return boards.updateTypeList(request)


# 开发板类型删除
@app.route('/delTypeList', methods=['POST'])
def delTypeList():
    return boards.delTypeList(request)


# 开发板列表获取
@app.route('/getBoardList', methods=['GET'])
def getBoardList():
    return boards.getBoardList(request)
    

# 开发板列表增加
@app.route('/insertBoardList', methods=['POST'])
def insertBoardList():
    return boards.insertBoardList(request)


# 开发板列表更新
@app.route('/updateBoardList', methods=['POST'])
def updateBoardList():
    return boards.updateBoardList(request)


# 开发板列表删除
@app.route('/delBoardList', methods=['POST'])
def delBoardList():
    return boards.delBoardList(request)


# 占用开发板
@app.route('/occBoard', methods=['POST'])
def occBoard():
    return boards.occBoard(request)


# 释放开发板
@app.route('/reBoard', methods=['POST'])
def reBoard():
    return boards.reBoard(request)


# 日志列表获取
@app.route('/getLogList', methods=['GET'])
def getLogList():
    return logs.getLogList(request)


# 日志列表清除
@app.route('/clearList', methods=['POST'])
def clearList():
    return logs.clearList(request)


# Admin获取
@app.route('/getAdminList', methods=['GET'])
def getAdminList():
    return admins.getAdminList(request)


# Admin增加
@app.route('/insertAdminList', methods=['POST'])
def insertAdminList():
    return admins.insertAdminList(request)


# Admin更新
@app.route('/updateAdminList', methods=['POST'])
def updateAdminList():
    return admins.updateAdminList(request)


# Admin删除
@app.route('/delAdminList', methods=['POST'])
def delAdminList():
    return admins.delAdminList(request)


# power ip 列表
@app.route('/getPowerList', methods=['GET'])
def powerList():
    return power.getPowerList(request)


# restartBoard
@app.route('/restartBoard', methods=['POST'])
def restartBoard():
    return power.restartBoard(request)

# restartImage
@app.route('/restartImage', methods=['POST'])
def restartImage():
    return reimage.restartImage(request)


# ping ip
@app.route('/pingIp', methods=['POST'])
def pingIp():
    # return power.pingIp(request)
    return power.pingR(request)



@socketio.on('connect')
def test_connect():
    # 客户端连接到服务器
    print('-----------Client connected------------')


@socketio.on('message')
def handle_terminal_message(message):
    # 处理从客户端接收到的消息
    print('-----------received message-----------: ' + message)
    command = message.strip()  # 获取客户端发送的命令并去除前后空格
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # 将结果发送回客户端
    socketio.emit('message', result.stdout)


@socketio.on('disconnect')
def test_disconnect():
    # 客户端从服务器断开连接
    print('-----------Client disconnected--------')



if __name__ == "__main__":
    # app.run()
    socketio.run(app)
