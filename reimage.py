import json
from flask import jsonify
import tools

def restartImage(request):
    ip = json.loads(request.get_data()).get('ip')
    path = json.loads(request.get_data()).get('image')
    print(ip, 'ip')
    print(path, 'path')
    if ip and path:
        res = tools.restart(path, ip)
    else:
        res = 'ip or path not found'
    return jsonify({"code": 200, "data": {"restartImage": res, 'user':tools.getUser() }})
    