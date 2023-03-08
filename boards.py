import db
import json
from flask import jsonify

def arrHandle(data):
    arr = []
    state = type(data) is dict


    print(data, '1111111')
    print(state, '2222222')


    if (state):
        obj = {"typeName": data.get('typeName'), "remark": data.get('remark')}
        arr.append(obj)
    else:
        data2 = list(data)
        print(data2, '33333333')
        for item in data2:
            print(item, '444444444')
            obj = {"typeName": item.get('typeName'), "remark": item.get('remark')}
            arr.append(obj)
    print(arr, '5555555')
    return arr


def getTypeList(request):
    get_data = request.args.to_dict()
    typeName = get_data.get('typeName')
    searchName = {"typeName" : { "$regex" : typeName}} if typeName else ''
    dbType = db.getDbData('web_system_db', 'board_type_list', searchName)
    typeInfo = arrHandle(dbType)
    return jsonify({"code": 200, "data": {"typeInfo": typeInfo }})


def addTypeList(request):
    typeName = json.loads(request.get_data()).get('typeName')
    remark = json.loads(request.get_data()).get('remark')
    state = db.insertDbData('web_system_db', 'board_type_list', {
                            "typeName": typeName, "remark": remark})
    if state:
        return jsonify({"code": 200, "message": "操作成功"})
    else:
        return jsonify({"code": 205, "message": "该类型已存在！"})
