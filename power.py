import json
from flask import jsonify
import tools
import logs
import copy
import db

    # with open('/group/xbjlab/dphi_edge/workspace/zboard/conf/zynq_hosts.json', 'r', encoding='utf-8') as f:

def getPowerList(request):
    with open('/group/xbjlab/dphi_edge/workspace/zboard/conf/zynq_hosts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify({"code": 200, "data": {"powerList": data }})


def restartBoard(request):
    ip = json.loads(request.get_data()).get('ip')
    id = json.loads(request.get_data()).get('id')
    opearUser = json.loads(request.get_data()).get('opearUser')
    insertData = list(db.getDbData('web_system_db', 'board_list', {"id": id}))
    insertData[0].update({'opearUser':opearUser})
    with open('/group/xbjlab/dphi_edge/workspace/zboard/conf/zynq_hosts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key in data.keys():
            if key == ip:
                item = data[key]
        if(not not item):
            res = tools.restart(item['power']['strip_addr'], item['power']['outlet'])
            logs.insertLogList('powerCycle', insertData)
            return jsonify({"code": 200, "data": {"powerList": res }})
        else:
            res = 'Reboot item data does not exist'
            return jsonify({"code": 200, "data": {"powerList": res }})
    

def pingIp(request):
    ip = json.loads(request.get_data()).get('ip')
    if not not ip:
        res = tools.ping_ip2(ip)
        return jsonify({"code": 200, "data": {"pingIp": res }})
    else:
        return jsonify({"code": 200, "data": {"pingIp": 'ip not found' }})