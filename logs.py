import db
import json
from flask import jsonify
import tools

def getLogList(request):
    get_data = request.args.to_dict()
    type = {"type": {"$in": get_data.get('type').split(',')}} if get_data.get('type') else ""
    operate = {"operate": {"$in": get_data.get('operate').split(',')}} if get_data.get('operate') else ""
    ip = {"ip": {"$regex": get_data.get('ip')}} if get_data.get('ip') else ""
    user = {"user": {"$regex": get_data.get('user')}} if get_data.get('user') else ""
    arr = [type, operate, ip, user]
    searchName = {}
    for item in arr:
        if not not item:
            searchName.update(item)
    dbType = db.getDbData('web_system_db', 'logs', searchName)
    typeInfo = tools.arrHandle(dbType, 'id', 'time', 'operate', 'user', 'ip', 'newIp', 'type', 'newType', "remark", "newRemark")
    return jsonify({"code": 200, "data": {"boardInfo": typeInfo }})


def insertLogList(opera, data, oldData):
    listInfo = tools.arrHandle(data, 'type', 'ip', 'remark')
    oldListInfo = tools.arrHandle(oldData,'id', 'type', 'ip', 'remark') if oldData else {"type": "", "ip": "", "remark": ""}
    listInfo[0].update({"operate": opera})
    if oldData:
        listInfo[0].update({"oldType": oldListInfo[0].get('type')})
        listInfo[0].update({"oldIp": oldListInfo[0].get('ip')})
        listInfo[0].update({"oldRemark": oldListInfo[0].get('remark')})
    
    print(listInfo, 'listInfolistInfo listInfo')

    db.insertDbData('web_system_db', 'logs', listInfo[0])
