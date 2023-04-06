from flask import Flask, request
import os
import subprocess

def arrHandle(data, *args):
    arr = []
    state = type(data) is dict
    if (state):
        obj = {}
        for i in list(args):
            if not not i:
                obj.update({i: data.get(i)})
        arr.append(obj)
    else:
        data2 = list(data)
        for item in data2:
            obj = {}
            for i in list(args):
                if not not i:
                    obj.update({i: item.get(i)})
            arr.append(obj)
    return arr

def create_flask_app():
    app = Flask(__name__)

    # 处理中文编码
    app.config['JSON_AS_ASCII'] = False
    return app


def getUser():
    name = subprocess.check_output(['sh', './getname.sh'])
    print('name是:', name.decode().strip())
    return name.decode().strip()


def restart(arg1, arg2):
    # # 设置脚本路径和参数
    # script_path = ''

    # # 执行脚本并获取输出结果
    # output = subprocess.run([script_path, arg1, arg2], capture_output=True, text=True)

    # # 将输出结果发送回前端
    # return output.stdout
    script_path = './restart.sh'
    cmd = [script_path, arg1, arg2]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f'Error: {stderr.decode("utf-8")}', 500

    return stdout.decode('utf-8')