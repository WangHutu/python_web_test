import json
from flask import jsonify
import tools
import logs
import time
import db
import threading

def restartImage(request):
    ip = json.loads(request.get_data()).get('ip')
    id = json.loads(request.get_data()).get('id')
    opearUser = json.loads(request.get_data()).get('opearUser')
    path = json.loads(request.get_data()).get('image')
    insertData = list(db.getDbData('web_system_db', 'board_list', {"id": id}))
    insertData[0].update({'opearUser':opearUser})
    if ip and path:
        with open('/group/xbjlab/dphi_edge/workspace/zboard/conf/zynq_hosts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in data.keys():
                if key == ip:
                    item = data[key]
            if(not not item):
                t = threading.Thread(target=tools.reimage(path, ip, item['server']))
                t.start()
                # res = tools.reimage(path, ip, item['server'])
                insertData[0].update({'flashLog': f'zboard.out.{ip}'})
                insertData[0].update({"flashTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
                logs.insertLogList('flashImage', insertData)
                return jsonify({"code": 200, "data": {"restartImage": '', 'user':tools.getUser() }})
            else:
                res = 'Reboot item data does not exist'
                return jsonify({"code": 200, "data": {"powerList": res, 'user':tools.getUser() }})
    else:
        res = 'ip or path not found'
        return jsonify({"code": 200, "data": {"restartImage": res, 'user':tools.getUser() }})
    