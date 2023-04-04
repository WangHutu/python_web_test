import db
import json
from flask import jsonify
import tools
import logs
import copy
import time


def getAdminList(request):
    get_data = request.args.to_dict()
    admin = get_data.get('admin')
    searchName = {"admin" : { "$regex" : admin}} if admin else ''
    dbType = db.getDbData('web_system_db', 'admin_list', searchName)
    adminInfo = tools.arrHandle(dbType, 'admin', 'remark', 'id')
    return jsonify({"code": 200, "data": {"adminInfo": adminInfo, 'user':tools.getUser() }})


def insertAdminList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    admin = json.loads(request.get_data()).get('admin')
    remark = json.loads(request.get_data()).get('remark')
    state = db.insertDbData('web_system_db', 'admin_list', {
                            "admin": admin, "remark": remark}, {"admin": admin}, 'admin')
    if state:
        return jsonify({"code": 200, "message": "Success"})
    else:
        return jsonify({"code": 205, "message": "该类型已存在！"})


def updateAdminList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，无插入数据"})
    id = json.loads(request.get_data()).get('id')
    remark = json.loads(request.get_data()).get('remark')
    state = db.updateDbData('web_system_db', 'admin_list', {"remark": remark}, {"id": id})
    if state:
        return jsonify({"code": 200, "message": "Success"})
    else:
        return jsonify({"code": 400, "message": "Error"})


def delAdminList(request):
    if (not json.loads(request.get_data())):
        return jsonify({"code": 200, "message": "操作失败，缺少相关数据"})
    id = json.loads(request.get_data()).get('id')
    state = db.delDbData('web_system_db', 'admin_list', { "id": id})
    if state:
        return jsonify({"code": 200, "message": "Success"})
    else:
        return jsonify({"code": 400, "message": "Error"})
    