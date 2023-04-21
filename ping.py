import subprocess
import json
import time
import datetime
import os

# 需要ping的IP列表
# ip_list = ['10.176.179.78', '10.176.179.143']
with open('/group/xbjlab/dphi_edge/workspace/zboard/conf/zynq_hosts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    ip_list = data.keys()

# 定义记录结果的json文件名和路径
json_file = 'ping_result.json'
json_path = os.path.join(os.path.dirname(__file__), json_file)


# 记录ping结果的字典
result_dict = {}
for ip in ip_list:
    # 使用subprocess模块启动ping命令，并传入参数ip
    result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True)
    # 将ping结果记录到result_dict字典中
    result_dict[ip] = 'success' if '1 received' in result.stdout else 'fail'
# 将result_dict字典写入json文件中
with open(json_path, 'w') as f:
    json.dump(result_dict, f)
# 每天凌晨3点清除json文件
if datetime.datetime.now().hour == 3 and datetime.datetime.now().minute == 0:
    os.remove(json_path)
