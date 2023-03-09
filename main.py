from flask import Flask, request
import registerLogin
import boards

app = Flask(__name__)


# 处理中文编码
app.config['JSON_AS_ASCII'] = False
 
 
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
    



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
