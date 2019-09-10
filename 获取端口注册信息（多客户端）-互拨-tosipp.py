#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 11:26
# @Author  : ray lei
# @File    : smsbank.py


import requests
from collections import Counter
from bs4 import BeautifulSoup
import re
from fabric.api import run, cd

"""
适配多台simbank进行互拨的场景，
优化simbank端口数据获取方式，

"""


def get_html(ip):
    '''
    通过url获取simbank当前状态信息
    返回html
     '''
    url = 'http://admin:admin@' + ip + \
        '/simproxy/ajax_server_simbank.php?&action=refresh_sim'
    respons = requests.get(url)
    html = respons.text
    return html
    # print(html)


def get_info(html, SM_name_list):
    '''
    解析html文件 找到需要的信息
    Serial_Number 参数通过查看simbank上的信息得到。按照设置注册simbank 中的排序情况 得出参数信息。
    返回information 信息列表
    '''
    soup = BeautifulSoup(html, 'lxml')
    Gw_port_phon_info = [] 
    for SM_name in SM_name_list:
        table = soup.find('table', attrs={'class':f'tshow {SM_name}'})  # 找到simbank序列号对应的web table，
        if table != None:     # 检查序列号是否存在 不为None 即序列号存在
            tag = table.find_all("div",class_="helptooltips") # 获取table里面所有的helptooltips信息
            print(f'<<< {SM_name} is',len(tag),">>>\n")   
            for t, s_p in zip(tag[0:20], range(1, 21)):
                """
                t   : 网页showhelp信息列表
                s_p : simbank 端口编号列表
                """
                img = t.find('img')
                status = str(img).split('led_')[1].split('.')[0]
                En_status = {'signal', 'idle', 'busy'}
                # print(status)
                if status in En_status:
                    t = str(t)
                    Phone_num = re.search("\d{3,15}<b", t)
                    Phone_num = Phone_num.group(0).replace("<b", "")
                    Gw_num = re.search("Sim No\.: \d+", t)
                    Gw_num = Gw_num.group(0).replace("Sim No.: ", "")
                    # Rest_time = re.search(" Time:\d+", t)## add Rest_time
                    # Rest_time = Rest_time.group(0).replace("Time:","")## add Rest_time

                    # Gw_port_phon_info.append([int(Gw_num), Phone_num,int(Rest_time)]) ## add Rest_time

                    Gw_port_phon_info.append([int(Gw_num), Phone_num])
                    print(
                        f'Simbank_port_Number: {s_p}\tGateway_port_Number: {Gw_num}\tPhone_Number: {Phone_num}\t\n')
                else:
                    pass
        else :
            print(f"<<< {SM_name} is Not Found >>>\n")
        

    return sorted(Gw_port_phon_info)
    # return sorted(Gw_port_phon_info,key=lambda x :x[2],reverse=True) ## add Rest_time 


def Print_rules(black_num,p):
    if len(black_num) > 1 & len(black_num) % 2 != 0:
        """传入的列表长度不为双数时 删除最后一个元素，使列表变为双数，以实现互拨"""
        black_num.pop()
    """从 列表中取出 port 和 num  分别操作"""
    port = [int(i[0]) for i in black_num]
    num = [int(i[1].strip()) for i in black_num]
    """将 port 和 num 各自分为两组"""
    port_1 = [port[i] for i in range(int(len(port)/2))]
    port_2 = [port[i] for i in range(int(len(port)/2), int(len(port)))]

    num_1 = [num[i] for i in range(int(len(port)/2))]
    num_2 = [num[i] for i in range(int(len(port)/2), int(len(port)))]

    """
    port1 对应 num2
    port2 对应 num1
    生成 拨号规则
    """
    f = open("call_1.csv",'w')
    f2 = open("call_2.csv",'w')
    print("SEQUENTIAL",file=f)
    print("SEQUENTIAL",file=f2)
    for i,j in zip(port_1,port_2):
        print(i,'\t<<<CALL>>>\t',j)

    print(f'前{len(port_1)}个端口呼叫规则')
    for i,j in zip(port_1,num_2):
        sip = 8000 + i
        if p == 1:
            print(f'{sip};{sip};[authentication username={sip} password=OpenVox2032-165];'+str(j),file=f)
        print(f'{sip};{sip};[authentication username={sip} password=OpenVox2032-165];'+str(j))

    print(f'后{len(port_2)}个端口呼叫规则')
    for i,j in zip(port_2,num_1):
        sip = 8000 + i
        if p == 1:
            print(f'{sip};{sip};[authentication username={sip} password=OpenVox2032-165];'+str(j),file=f2)
        print(f'{sip};{sip};[authentication username={sip} password=OpenVox2032-165];'+str(j))
    f.close()
    f2.close()

def main(ip,SM_list):
    html = get_html(ip) #获取网页数据
    Gw_port_phon_info =  get_info(html,SM_list) #分析数据，提取simbank端口、网关端口、网关电话号码信息
    Print_rules(Gw_port_phon_info,1)  #将信息组合后 Print 到终端

if __name__ == '__main__':
    ip = '172.16.6.166'
    SM_list = ["TACQ2AAB","TACQ2AJG","aa"] #  6.166："TACQ2AAB" 6.167："TACQ2AJG"
    main(ip,SM_list)