import db
import json
from flask import jsonify
import tools
import logs
import copy


def getTypeList(request):
    get_data = request.args.to_dict()
    typeName = get_data.get('typeName')
    searchName = {"typeName" : { "$regex" : typeName}} if typeName else ''
    dbType = db.getDbData('web_system_db', 'board_type_list', searchName)
    typeInfo = tools.arrHandle(dbType, 'typeName', 'remark', 'id')
    return jsonify({"code": 200, "data": {"typeInfo": typeInfo, 'user':tools.getUser() }})


def insertTypeList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    typeName = json.loads(request.get_data()).get('typeName')
    remark = json.loads(request.get_data()).get('remark')
    state = db.insertDbData('web_system_db', 'board_type_list', {
                            "typeName": typeName, "remark": remark}, {"typeName": typeName}, 'typeName')
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 205, "message": "该类型已存在！"})


def updateTypeList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    id = json.loads(request.get_data()).get('id')
    remark = json.loads(request.get_data()).get('remark')
    state = db.updateDbData('web_system_db', 'board_type_list', {"remark": remark}, {"id": id})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 400, "message": "操作失败"})


def delTypeList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，缺少相关数据"})
    id = json.loads(request.get_data()).get('id')
    state = db.delDbData('web_system_db', 'board_type_list', { "id": id})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 400, "message": "操作失败"})
    

def getBoardList(request):
    get_data = request.args.to_dict()
    type = {"type": {"$in": get_data.get('type').split(',')}} if get_data.get('type') else ""
    status = {"status": get_data.get('status')} if get_data.get('status') else ""
    ip = {"ip": {"$regex": get_data.get('ip')}} if get_data.get('ip') else ""
    arr = [type, status, ip]
    searchName = {}
    for item in arr:
        if not not item:
            searchName.update(item)
    dbType = db.getDbData('web_system_db', 'board_list', searchName)
    typeInfo = tools.arrHandle(dbType, 'type', 'status', 'ip', 'remark', 'id')
    return jsonify({"code": 200, "data": {"boardInfo": typeInfo, 'user':tools.getUser() }})


def insertBoardList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    insertData = {
        "type": json.loads(request.get_data()).get('type'),
        "ip": json.loads(request.get_data()).get('ip'),
        "status": json.loads(request.get_data()).get('status'),
        "remark": json.loads(request.get_data()).get('remark') if json.loads(request.get_data()).get('remark') else ""
    }
    state = db.insertDbData('web_system_db', 'board_list', insertData, {"ip": insertData.get('ip')}, 'ip')
    if state:
        logs.insertLogList('add', insertData)
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 206, "message": "IP已存在 !"})
    

def updateBoardList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    oldIp = json.loads(request.get_data()).get('oldIp')
    id = json.loads(request.get_data()).get('id')
    insertData = {
        "type": json.loads(request.get_data()).get('type'),
        "ip": json.loads(request.get_data()).get('ip'),
        "status": json.loads(request.get_data()).get('status'),
        "remark": json.loads(request.get_data()).get('remark')
    }
    oldData = copy.deepcopy(list(db.getDbData('web_system_db', 'board_list', {"id": id})))
    print(tools.arrHandle(oldData), 'oldData')
    state = db.updateDbData('web_system_db', 'board_list', insertData, {"id": id})
    if state:
        logs.insertLogList('update', insertData, oldData)
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 400, "message": "操作失败"})


def delBoardList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，缺少相关数据"})
    id = json.loads(request.get_data()).get('id')
    state = db.delDbData('web_system_db', 'board_list', {"id": id})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 400, "message": "操作失败"})