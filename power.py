import db
import json
from flask import jsonify
import tools


def getPowerList(request):
    with open('/group/xbjlab/dphi_edge/workspace/zboard/conf/zynq_hosts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify({"code": 200, "data": {"powerList": data, 'user':tools.getUser() }})


def restartBoard(request):
    ip = json.loads(request.get_data()).get('ip')
    print(ip, 'ip')
    with open('zynq_hosts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key in data.keys():
            if key == ip:
                item = data[key]
        if(not not item):
            print(item, 'item')
            print(item['power']['strip_addr'])
            print(item['power']['outlet'])
            res = tools.restart(item['power']['strip_addr'], item['power']['outlet'])
            return jsonify({"code": 200, "data": {"powerList": res, 'user':tools.getUser() }})
        else:
            res = 'Reboot item data does not exist'
            return jsonify({"code": 200, "data": {"powerList": res, 'user':tools.getUser() }})
    