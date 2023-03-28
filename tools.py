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
    name = subprocess.check_output(['./getname.sh'])
    print('name是:', name.decode().strip())
    return name.decode().strip()