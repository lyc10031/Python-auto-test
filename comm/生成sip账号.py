#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 11:16
# @Author  : ray lei
# @File    : 生成sip账号.py
# @Software: PyCharm


def sip_account(sip_type,first_number,total,host=None):
    gw_sip = 'gw_sip = '
    for i in range(1,1+int(total)):
        # gw_sip += f'gw_sip_{i};'
        if i < int(total):
            gw_sip += f'gw_sip_{i};'
        else:
            gw_sip += f'gw_sip_{i}'
    """ 打印到终端 """
    print(gw_sip)  
    for i in range(1, 1+total):
        num = int(first_number) + i
        if host != None:
            print(f'gw_sip_{str(i)} = {sip_type};{num};{num};123456;{host};')
        else:
            print(f'gw_sip_{str(i)} = {sip_type};{num};{num};123456;;')
    """ 打印到文件中 """
    with open('web_cases.conf','w') as f:
        print('[test_sip_endpoint]',file=f)
        print(gw_sip,file=f)
        for i in range(1, 1+total):
            num = int(first_number) + i
            if host != None:
                print(f'gw_sip_{str(i)} = {sip_type};{num};{num};123456;{host};',file=f)
            else:
                print(f'gw_sip_{str(i)} = {sip_type};{num};{num};123456;;',file=f)

sip_account('server',8000,32)  # 生成server账号

# sip_account('client',8000,16,'172.16.80.133')   # 生成client账号
