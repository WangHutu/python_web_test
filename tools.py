from flask import Flask, jsonify
import os
import subprocess
from subprocess import check_call, check_output, CalledProcessError

def arrHandle(data, *args):
    arr = []
    state = type(data) is dict
    if (state):
        obj = {}
        for i in list(args):
            if not not i:
                obj.update({i: data.get(i)})
        arr.append(obj)
    else:
        data2 = list(data)
        for item in data2:
            obj = {}
            for i in list(args):
                if not not i:
                    obj.update({i: item.get(i)})
            arr.append(obj)
    return arr


def create_flask_app():
    app = Flask(__name__)

    # 处理中文编码
    app.config['JSON_AS_ASCII'] = False
    return app


def getUser():
    name = subprocess.check_output(['sh', './getname.sh'])
    # print('name是:', name.decode().strip())
    return name.decode().strip()


def restart(arg1, arg2):
    # 设置脚本路径和参数
    script_path = './restart.sh'

    print(f'cmd: sh {script_path} {arg1} {arg2}')
    # 执行脚本并获取输出结果
    output = subprocess.run(['sh', script_path, arg1, arg2], capture_output=True, text=True)

    # 将输出结果发送回前端
    return output.stdout


def reimage_test(arg1, arg2):
    # 设置脚本路径和参数
    script_path = './reImage.sh'
    print(f'cmd: sh {script_path} {arg1} {arg2}')
    # 执行脚本并获取输出结果
    output = subprocess.run(['sh', script_path, arg1, arg2], capture_output=True, text=True)

    # 将输出结果发送回前端
    return output.stdout

def reimage(arg1, arg2, server):
    #cmd_tmp = ". /group/xbjlab/dphi_edge/workspace/vitis_2022.2/settings64.sh; xsdb /group/xbjlab/dphi_edge/workspace/zboard/board_data/vek280/jtag_boot_linux_no_image.tcl"
    #cmd = '/bin/bash -c "%s"' % cmd_tmp
    if server=='xbjlabdpsvr02':
        cmd = "rm *%s*; /group/xbjlab/dphi_edge/workspace/zboard/bin/zboard run-test -m jtag_dual_linux -i %s -e test.sh --ip %s --interactive" % (arg2, arg1, arg2)
    else:
        cmd="rm zboard.out.%s; ssh %s 'cd /tmp/; /group/xbjlab/dphi_edge/workspace/zboard/bin/zboard run-test -m jtag_dual_linux -i %s -e test.sh --ip %s --interactive'" % (arg2, server, arg1, arg2)
    print(f'cmd: {cmd}')
    check_call(cmd,shell=True)
    print(f'zboard.out.{arg2}')



def ping_ip(ip):
    # 构造 ping 命令
    cmd = ['sh', 'ping', '-c', '3', ip]
    # 执行 ping 命令
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 解析 ping 命令的输出
    if output.returncode == 0:
        # 如果返回码为 0，表示 ping 成功，返回 True
        return True
    else:
        # 如果返回码不为 0，表示 ping 失败，返回 False
        return False
    

def ping_ip2(ip):
    # 执行 ping 命令并返回结果
    cmd = f'ping -c 3 {ip}'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = p.communicate()
    if error:
        return {'error': error.decode()}
    else:
        return {'success': output.decode()}
