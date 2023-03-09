from flask import jsonify
import json
import db
import tokenJwt


def register(request):
    # 请求头是 json 用 request.get_data() 获取参数
    user = json.loads(request.get_data()).get('user')
    password = json.loads(request.get_data()).get('password')
    state = db.insertDbData('web_system_db', 'users', {"user": user, "password": password}, {"user": user})
    if state:
        return jsonify({"code": 200, "message": "注册成功, 请登录"})
    else:
        return jsonify({"code": 205, "message": "该用户已存在！"})
    

def login(request):
    # 请求头是 json 用 request.get_data() 获取参数
    user = json.loads(request.get_data()).get('user')
    password = json.loads(request.get_data()).get('password')
    dbUser = db.getDbData('web_system_db', 'users', {"user": user})
    print(dbUser, '数据库中查询出来的数据')
    if dbUser:
        if password == dbUser.get('password'):
            token = tokenJwt.create_token(user, password)
            return jsonify({"code": 200, "message": "success !", "data": {"token": token, "info": {'user': dbUser.get('user'), 'password': dbUser.get('password')}}})
        else:
            return jsonify({"code": 201, "message": "密码不正确"})
    else:
        return jsonify({"code": 204, "message": "用户不存在"})