#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 11:26
# @Author  : ray lei
# @File    : smsbank.py



import requests
from collections import Counter
from bs4 import BeautifulSoup
import re
from fabric.api import run,cd

"""
电信卡呼叫信息，生成sipp配置文件
电信卡需要互拨来进行测试
"""


def get_html(ip):
    '''
    通过url获取simbank当前状态信息
    返回html
     '''
    url = 'http://admin:admin@' + ip + '/simproxy/ajax_server_simbank.php?&action=refresh_sim'
    respons = requests.get(url)
    html = respons.text
    return html
    # print(html)

def get_info(html,Serial_Number=2):
    '''
    解析html文件 找到需要的信息
    Serial_Number 参数通过查看simbank上的信息得到。按照设置注册simbank 中的排序情况 得出参数信息。
    返回information 信息列表
    '''
    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find_all('div', class_='helptooltips')
    # print(type(Serial_Number))
    information_black = []    
    information_red = []
    # print(tag)
    if Serial_Number == 1:      #根据实际的simbank 端口数量进行修改。
        tag2 = tag[0:127]       #每个simbank 默认有128个端口。第一个simbank 是0-127 第二个是128-255 第三个是256-383
    elif Serial_Number == 2:
        # print(type(Serial_Number))
        tag2 = tag[128:255]
    else:
        tag2 = tag[256:]
    # print(tag2)

    for t,s_p in zip(tag2[0:24],range(1,25)):
        """选择当前simbank的端口0-17代表1到16端口"""

        img = t.find('img')
        status = str(img).split('led_')[1].split('.')[0]
        En_status = {'signal','idle','busy'}
        # print(status)
        if status in En_status:
            t = str(t)
            port_info = re.findall(r'[0-9]+', t)
            # print(port_info)

            # Gateway_port_Nu = [k for k,v in dict(Counter(port_info)).items() if v >1][0]
            ''' Counter 方法返回 dict(Counter(port_info)) 返回（元素：及元素出现次数）的键值对 '''
            # Phone_Nu = max(port_info, key=len)


            Gateway_port_Nu = port_info[6]
            Phone_Nu = max(port_info, key=len)
            # Simban_num = port_info[
            # if s_p > 16:
            #     '''电信卡：前16个端口插得是黑色号码的卡，后面的卡是红色号码，需要分开互打。黑色打黑色，红色打红色'''
            #     information_red.append([int(Gateway_port_Nu), Phone_Nu])
            # else:
            #     information_black.append([int(Gateway_port_Nu), Phone_Nu])

            information_black.append([int(Gateway_port_Nu), Phone_Nu])
            print(f'Simbank_port_Number: {s_p}\tGateway_port_Number: {Gateway_port_Nu}\tPhone_Number: {Phone_Nu}\t\n')
            # print(port_info)
            # print('<------------->')
        else:
            pass

    return sorted(information_black),sorted(information_red)



def cucc_local_print(black_num):
    if len(black_num) % 2  != 0:
        """传入的列表不为双数时 删除最后一个元素，使列表变为双数，以实现互拨"""
        black_num.pop()
    


    port = [int(i[0]) for i in black_num ]
    num = [int(i[1].strip()) for i in black_num ]

    port_1 = [port[i] for i in range(int(len(port)/2))]
    port_2 = [port[i] for i in range(int(len(port)/2),int(len(port)))]

    num_1 = [num[i] for i in range(int(len(port)/2))]
    num_2 = [num[i] for i in range(int(len(port)/2),int(len(port)))]


    for i,j in zip(port_1,port_2):
        print(i,'\t<<<CALL>>>\t',j)

    print(f'前{len(port_1)}个端口呼叫规则')
    with open('auto_call_test.csv','w') as f:
        # print('SEQUENTIAL',file=f)
        for i,j in zip(port_1,num_2):
            sip = 8000 + i
            print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j))
            # print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j),file=f)

    print(f'后{len(port_2)}个端口呼叫规则')
    for i,j in zip(port_2,num_1):
        sip = 8000 + i
        # sip = '1001'
        print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j))

def cucc_to_sipp(black_num):
    if len(black_num) % 2  != 0:
        black_num.pop()
    
    # html = get_html(ip)
    # black_num,red_num = get_info(html,1) 
    # print(black_num)
    """从 列表中取出 port 和 num  分别操作"""
    port = [int(i[0]) for i in black_num ]
    num = [int(i[1].strip()) for i in black_num ]
    """将 port 和 num 各自分为两组"""
    port_1 = [port[i] for i in range(int(len(port)/2))]
    port_2 = [port[i] for i in range(int(len(port)/2),int(len(port)))]

    num_1 = [num[i] for i in range(int(len(port)/2))]
    num_2 = [num[i] for i in range(int(len(port)/2),int(len(port)))]

    """ 
    port1 对应 num2 
    port2 对应 num1 
    生成 拨号规则
    """

    with open('auto_call_test.csv','w') as f:
        print('SEQUENTIAL',file=f)
        for i,j in zip(port_1,num_2):
            sip = 8000 + i
            # print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j))
            print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j),file=f)

    # print(f'后{len(port_2)}个端口呼叫规则')
    # for i,j in zip(port_2,num_1):
    #     sip = 8000 + i
    #     # sip = '1001'
    #     print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j))


def cmcc_print(black_num):
    if len(black_num) > 1 and len(black_num) % 2  != 0:
        """传入的列表不为双数时 删除最后一个元素，使列表变为双数，以实现互拨"""
        black_num.pop()
    


    port = [int(i[0]) for i in black_num ]
    num = [int(i[1].strip()) for i in black_num ]

    port_1 = [port[i] for i in range(int(len(port)/2))]
    port_2 = [port[i] for i in range(int(len(port)/2),int(len(port)))]

    num_1 = [num[i] for i in range(int(len(port)/2))]
    num_2 = [num[i] for i in range(int(len(port)/2),int(len(port)))]


    for i,j in zip(port_1,port_2):
        print(i,'\t<<<CALL>>>\t',j)

    print(f'前{len(port_1)}个端口呼叫规则')
    with open('/home/ray/SIPp/SIPp_test/auto_call_test.csv','w') as f:
        # print('SEQUENTIAL',file=f)
        for i,j in zip(port_1,num_2):
            sip = 8000 + i
            print(f'{sip};{sip};[authentication username={sip} password=123456];'+'1008619' )
            # print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j),file=f)

    print(f'后{len(port_2)}个端口呼叫规则')
    for i,j in zip(port_2,num_1):
        sip = 8000 + i
        # sip = '1001'
        print(f'{sip};{sip};[authentication username={sip} password=123456];'+'1008619')

def cmcc_to_sipp(black_num):
    if len(black_num) % 2  != 0:
        black_num.pop()
    
    # html = get_html(ip)
    # black_num,red_num = get_info(html,1) 
    # print(black_num)
    """从 列表中取出 port 和 num  分别操作"""
    port = [int(i[0]) for i in black_num ]
    num = [int(i[1].strip()) for i in black_num ]
    """将 port 和 num 各自分为两组"""
    port_1 = [port[i] for i in range(int(len(port)/2))]
    port_2 = [port[i] for i in range(int(len(port)/2),int(len(port)))]

    num_1 = [num[i] for i in range(int(len(port)/2))]
    num_2 = [num[i] for i in range(int(len(port)/2),int(len(port)))]

    """ 
    port1 对应 num2 
    port2 对应 num1 
    生成 拨号规则
    """

    with open('/home/ray/SIPp/SIPp_test/auto_call_test.csv','w') as f:
        print('SEQUENTIAL',file=f)
        for i in port:
            sip = 8000 + i
            # print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j))
            print(f'{sip};{sip};[authentication username={sip} password=123456];'+'1008619',file=f)

    # print(f'后{len(port_2)}个端口呼叫规则')
    # for i,j in zip(port_2,num_1):
    #     sip = 8000 + i
    #     # sip = '1001'
    #     print(f'{sip};{sip};[authentication username={sip} password=123456];'+str(j))

def main(ip):
    html = get_html(ip)
    black_num,red_num = get_info(html,1) 

    cucc_local_print(black_num)  #print 到终端

    # cucc_to_sipp(black_num)  #将配置写入到sipp的(.csv)呼叫文件中。

    # cmcc_print(black_num)
    # cmcc_to_sipp(black_num)


if __name__ == '__main__':
    ip = '172.16.6.169'
    main(ip)