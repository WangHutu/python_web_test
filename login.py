from flask import g, Flask, request, jsonify
import json
import jwt
import datetime
import db

app = Flask(__name__)


# 处理中文编码
app.config['JSON_AS_ASCII'] = False
 
 
# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'

# 构造header
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

SALT = "o7l8_t9bf"

def create_token(user, password):
    """
    生成jwt
    :param user: user
    :param password: password
    :return: token
    """
    # 构造payload
    payload = {
        'user': user,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    return result

def verify_jwt(token, secret=SALT):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.exceptions.ExpiredSignatureError:  # 'token已失效'
        return 1
    except jwt.DecodeError:  # 'token认证失败'
        return 2
    except jwt.InvalidTokenError:  # '非法的token'
        return 3


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    # 请求头是 json 用 request.get_data() 获取参数
    user = json.loads(request.get_data()).get('user')
    password = json.loads(request.get_data()).get('password')
    dbUser = db.getDbData('system', 'users', {"user": user})
    print(dbUser)
    if dbUser:
        if password == dbUser.get('password'):
            token = create_token(user, password)
            return jsonify({"code": 200, "message": "success !", "data": {"token": token, "info": {'user': dbUser.get('user'), 'password': dbUser.get('password')}}})
        else:
            return jsonify({"code": 201, "message": "密码不正确"})
    else:
        return jsonify({"code": 204, "message": "用户不存在"})
    


# 注册接口
@app.route('/register', methods=['POST'])
def register():
    # 请求头是 json 用 request.get_data() 获取参数
    user = json.loads(request.get_data()).get('user')
    password = json.loads(request.get_data()).get('password')
    state = db.insertDbData('system', 'users', {"user": user, "password": password})
    if state:
        return jsonify({"code": 200, "message": "注册成功, 请登录"})
    else:
        return jsonify({"code": 205, "message": "该用户已存在！"})
    



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
