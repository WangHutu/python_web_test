import db
import json
from flask import jsonify


def getTypeList(request):
    print(json.loads(request.get_data("typeName")), 'request')
    typeName = json.loads(request.get_data()).get('typeName') if json.loads(request.get_data()).get('typeName') else ''
    search = {"typeName": typeName} if typeName else False
    print(search,'search')
    dbType = db.getDbData('web_system_db', 'board_type_list', search)
    print(dbType, 'board_type_list')
    print(type(dbType), 'board_type_list')
    return jsonify({"code": 200, "data": dbType})


def addTypeList(request):
    typeName = json.loads(request.get_data()).get('typeName')
    remark = json.loads(request.get_data()).get('remark')
    state = db.insertDbData('web_system_db', 'board_type_list', {
                            "typeName": typeName, "remark": remark})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 205, "message": "该类型已存在！"})
