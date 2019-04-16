#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/28 14:56
# @Author  : ray lei
# @File    : 发命令.py
# @Software: PyCharm


import time
import paramiko,subprocess
from datetime import datetime
import threading

t1 = time.time()
th1 = []

def send_command(host,port,username,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,port=int(port),username=username,password=password)
    # stdin, stdout, stderr = ssh.exec_command('ls -l /proc/dahdi |grep "^-"| wc -l')
    # stdin, stdout, stderr = ssh.exec_command('')
    as_string = subprocess.check_output(["virsh", "list", "--state-running", "--name"], universal_newlines=True).strip()

    try:
        # info = stdout.read().decode('UTF-8')
        
        # print(host+'-->',info)
        print(f'{host}-->{as_string}')
        # return info
    except Exception as e:
        print(e)
    # ssh.exec_command('reboot')
    finally:
        ssh.close()

def warps(func):
    def deco(*args):
        t1 = time.time()
        f = func(*args)
        print(time.time() - t1)
        # return f
    return deco

# @warps
# def my_thread(h):
#     args = h.split(';')
#     print(args)
#     host = args[0]
#     port = args[1]
#     user = args[2]
#     password = args[3]
#     t = threading.Thread(target=send_command,args=(host,port,user,password,))
#     t.start()
#     th1.append(t)
def my_thread(h):
    args = h.split(';')
    print(args)
    host = args[0]
    port = 22
    user = args[1]
    password = args[2]
    t = threading.Thread(target=send_command,args=(host,port,user,password,))
    t.start()
    th1.append(t)

# @warps
def main(ip_list):
    # with open('ip_info.conf','r') as IP:
    #     ip_info1 = IP.read()
    # # ip_info = re.sub('\t', '',str(ip_info1))
    # ip_list = ip_info1.split("\n")
    # print(ip_list,len(ip_list))
    [my_thread(i) for i in ip_list]


if __name__ == '__main__':
    # IP_info = [
    #     '172.16.80.142;22;root;111111','172.16.80.133;22;root;111111',
    #     '172.16.80.150;22;root;111111','172.16.80.134;22;root;111111',
    #     '172.16.100.93;12345;super;admin','172.16.253.110;22;root;111111',
    # ]
    # ip1 = ['172.16.0.7;22;root;openvox2008', '172.16.0.69;22;root;OpenVoxSugarCRM', '172.16.0.25;22;root;OpenVoxERPserver', '172.16.33.109;22;root;111111', '172.16.6.130;22;root;111111', '172.16.6.98;22;root;111111', '172.16.73.100;22;root;111111', '172.16.6.152;22;root;111111', '172.16.88.69;22;root;111111', '172.16.0.3;22;root;OpenVox_jira20!7', '172.16.6.129;22;root;111111', '172.16.0.8;22;admin;hipchat', '172.16.0.33;22;root;openvox20!!']
    # ip3 = ['172.16.0.7;root;openvox2008', '172.16.0.69;root;OpenVoxSugarCRM', '172.16.0.25;root;OpenVoxERPserver', '172.16.33.109;root;111111', '172.16.6.130;root;111111', '172.16.6.98;root;111111', '172.16.73.100;root;111111']
    #
    #
    # ip2 = ['172.16.0.1;22;root;zhimakaimen']
    ip111 = ["172.16.0.116;root;openvox20!7","172.16.0.18;root;openvox20!3","172.16.0.26;root;openvox20!3"]
    test = ["172.16.80.142;root;111111"]
    # main(ip111)
    send_command('172.16.1.95',22,'op','111111')

