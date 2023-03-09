import db
import json
from flask import jsonify

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


def getTypeList(request):
    get_data = request.args.to_dict()
    typeName = get_data.get('typeName')
    searchName = {"typeName" : { "$regex" : typeName}} if typeName else ''
    dbType = db.getDbData('web_system_db', 'board_type_list', searchName)
    typeInfo = arrHandle(dbType, 'typeName', 'remark')
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
    

def getBoardList(request):
    get_data = request.args.to_dict()
    print(get_data, 'get_data')
    type = {"type": get_data.get('type')} if get_data.get('type') else ""
    status = {"status": get_data.get('status')} if get_data.get('status') else ""
    ip = {"ip": {"$regex": get_data.get('ip')}} if get_data.get('ip') else ""
    arr = [type, status, ip]
    searchName = {}
    for item in arr:
        if not not item:
            searchName.update(item)
    dbType = db.getDbData('web_system_db', 'board_list', searchName)
    typeInfo = arrHandle(dbType, 'type', 'status', 'ip')
    return jsonify({"code": 200, "data": {"boardInfo": typeInfo }})
