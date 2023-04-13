import db
import json
from flask import jsonify
import tools
import time

def getLogList(request):
    get_data = request.args.to_dict()
    type = {"type": {"$in": get_data.get('type').split(',')}} if get_data.get('type') else ""
    operate = {"operate": get_data.get('operate')} if get_data.get('operate') else ""
    ip = {"ip": {"$regex": get_data.get('ip')}} if get_data.get('ip') else ""
    user = {"user": {"$regex": get_data.get('user')}} if get_data.get('user') else ""
    arr = [type, operate, ip, user]
    searchName = {}
    for item in arr:
        if not not item:
            searchName.update(item)
    dbType = db.getDbData('web_system_db', 'logs', searchName)
    typeInfo = tools.arrHandle(dbType, 'id', 'time', 'operate', 'user', 'ip', 'newIp','image', 'newImage', 'number', 'newNumber', 'type', 'newType', "remark", "newRemark", 'opearUser')
    return jsonify({"code": 200, "data": {"boardInfo": typeInfo, 'user':tools.getUser() }})


def insertLogList(opera, data, oldData=''):
    newListInfo = tools.arrHandle(data, 'type', 'ip', 'remark', 'image', 'number', 'user', 'opearUser')
    oldListInfo = tools.arrHandle(oldData, 'type', 'ip', 'remark', 'image', 'number') if not not oldData else False
    
    # print(newListInfo, 'newListInfo')
    # print(oldListInfo, 'oldListInfo')

    insertData = {}
    insertData.update({"operate": opera})
    insertData.update({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    if not not oldListInfo:
        insertData.update({"type": oldListInfo[0].get('type')})
        insertData.update({"ip": oldListInfo[0].get('ip')})
        insertData.update({"number": oldListInfo[0].get('number')})
        insertData.update({"image": oldListInfo[0].get('image')})
        insertData.update({"remark": oldListInfo[0].get('remark')})

    insertData.update({"newType": newListInfo[0].get('type')})
    insertData.update({"newIp": newListInfo[0].get('ip')})
    insertData.update({"newNumber": newListInfo[0].get('number')})
    insertData.update({"newImage": newListInfo[0].get('image')})
    insertData.update({"newRemark": newListInfo[0].get('remark')})
    insertData.update({"user": newListInfo[0].get('user')})
    insertData.update({"opearUser": newListInfo[0].get('opearUser')})

    db.insertDbData('web_system_db', 'logs', insertData)



def clearList(request):
    state = db.delDbData('web_system_db', 'logs')
    if state:
        return jsonify({"code": 200, "message": "Success"})
    else:
        return jsonify({"code": 400, "message": "Error"})
