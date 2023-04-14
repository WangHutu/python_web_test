import json
from flask import jsonify
import tools
import logs
import copy
import db

def restartImage(request):
    ip = json.loads(request.get_data()).get('ip')
    id = json.loads(request.get_data()).get('id')
    opearUser = json.loads(request.get_data()).get('opearUser')
    path = json.loads(request.get_data()).get('image')
    insertData = list(db.getDbData('web_system_db', 'board_list', {"id": id}))
    insertData[0].update({'opearUser':opearUser})
    if ip and path:
        res = tools.reimage2(path, ip)
        logs.insertLogList('flashImage', insertData)
        return jsonify({"code": 200, "data": {"restartImage": '', 'user':tools.getUser() }})
    else:
        res = 'ip or path not found'
        return jsonify({"code": 200, "data": {"restartImage": res, 'user':tools.getUser() }})
    