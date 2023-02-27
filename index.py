from flask import Flask, request, jsonify
import json

app = Flask(__name__)


users_list = {"runfengw": ["123"],
              "huizhang": ["123"]}


@app.route('/login', methods=['POST'])
def check():
    # 请求头是 json 用 request.get_data() 获取参数
    user = json.loads(request.get_data()).get('user')
    password = json.loads(request.get_data()).get('password')
    print(user)
    print(password)
    if user and password:
        if user in users_list:
            info = users_list[user]
            if password == info[0]:
                return jsonify({"code": 200, "message": "登录成功！"})
            else:
                return jsonify({"code": 10001, "message": "密码不正确"})
        else:
            return jsonify({"code": 10002, "message": "用户不存在"})
    else:
        return jsonify({"code": 10003, "message": "用户名或密码为空", "user":user, "password":password})



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
