#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 9:49
# @Author  : ray lei
# @File    : 绑定sip_port.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.firefox.options import Options

options = Options()

options.headless = True

d = webdriver.Firefox(options=options) # headless 模式



def sip_sim_binding(d,port,num,gw_type):
    '''
    1、传入webdriver对象,
    2、端口数,
    3、起始sip编号，如果第一个sip是8001 那么就传入8000'''
    time.sleep(1)
    if gw_type == "gsm":
        d.find_element_by_link_text('ROUTING').click()
    elif gw_type == "analog":
        d.find_element_by_link_text('ANALOG').click()

    time.sleep(0.5)

    # 定位BCR 链接
    try:
        BCR = d.find_element_by_link_text('Batch Creating Rules')
    except:
        pass
    try:
        BCR = d.find_element_by_link_text('Batch Creat Rules')
    except:
        pass

    BCR.click()
    for i in range(1, int(port) + 1 ):
        ele = d.find_element_by_xpath('//*[@id="associated_chnnl1%s"]' % i)
        d.execute_script("arguments[0].scrollIntoView();", ele)
        Select(ele).select_by_visible_text(str(int(num)+i))
    try:
        d.find_element_by_xpath('//*[@value="Save"]').click()
    except:
        print('没有保存')
    time.sleep(1)
    try:
        d.find_element_by_id('apply').click()
    except:
        print('aaa')

def main(ip,port,num,gw_type='gsm'):
    url = 'http://admin:admin@' + ip
    d = webdriver.Firefox()
    # options = Options()

    # options.headless = True 

    # d = webdriver.Firefox(options=options) # headless 模式


    d.get(url)
    d.set_window_size(1024,768)
    try:
        d.find_element_by_xpath('//*[@id="modal-51"]/div/div/div[3]/button[1]').click()
    except:
        pass
    sip_sim_binding(d,port,num,gw_type)
    d.close()

if __name__ == '__main__':
    gw_type = "analog"
    ip = '172.16.6.165'
    main(ip,32,8000)

