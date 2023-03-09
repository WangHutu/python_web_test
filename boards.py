import db
import json
from flask import jsonify

def arrHandle(data):
    arr = []
    state = type(data) is dict
    if (state):
        obj = {"typeName": data.get('typeName'), "remark": data.get('remark')}
        arr.append(obj)
    else:
        data2 = list(data)
        for item in data2:
            obj = {"typeName": item.get('typeName'), "remark": item.get('remark')}
            arr.append(obj)
    return arr


def getTypeList(request):
    get_data = request.args.to_dict()
    typeName = get_data.get('typeName')
    searchName = {"typeName" : { "$regex" : typeName}} if typeName else ''
    dbType = db.getDbData('web_system_db', 'board_type_list', searchName)
    typeInfo = arrHandle(dbType)
    return jsonify({"code": 200, "data": {"typeInfo": typeInfo }})


def insertTypeList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    typeName = json.loads(request.get_data()).get('typeName')
    remark = json.loads(request.get_data()).get('remark')
    state = db.insertDbData('web_system_db', 'board_type_list', {
                            "typeName": typeName, "remark": remark}, {"typeName": typeName})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 205, "message": "该类型已存在！"})


def updateTypeList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    typeName = json.loads(request.get_data()).get('typeName')
    remark = json.loads(request.get_data()).get('remark')
    state = db.updateDbData('web_system_db', 'board_type_list', {"remark": remark}, {"typeName": typeName})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 400, "message": "操作失败"})


def delTypeList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    typeName = json.loads(request.get_data()).get('typeName')
    remark = json.loads(request.get_data()).get('remark')
    state = db.delDbData('web_system_db', 'board_type_list', { "typeName": typeName, "remark": remark})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 400, "message": "操作失败"})
