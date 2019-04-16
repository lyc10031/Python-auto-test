#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/29 18:01
# @Author  : ray lei
# @File    : 注册sip.py
# @Software: PyCharm



from python_lib.web_fun.lib import gateway_func
from selenium import webdriver
import configparser,time
import itertools


def get_element(driver,file,gw_type):
    sip_fun = gateway_func.endpoint_func(driver, gw_type) # 模拟网关： analog  其他 gsm
    # sip_fun.delete_all_endpoints()
    cfg = configparser.ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(itertools.chain(['[global]'], fp), source=file)

    # config.read(file,encoding='utf-8')
    gw_sip = cfg.get('test_sip_endpoint','gw_sip')
    gw_sip_num = gw_sip.split(';')
    for el in gw_sip_num:
        args = cfg.get('test_sip_endpoint', el).split(';')
        try:
            sip_fun.add_sip_endpoint(*args)
        except:
            print('创建账号： \n %s \n 失败！！！' % (args))
    print('totle ',len(gw_sip_num),'sip_endpoint...')

def manin(host,gw_type):
    url = 'http://admin:admin@' + host
    d = webdriver.Firefox()
    d.set_window_size(1024,768)
    d.get(url)
    try:
        d.find_element_by_xpath('//*[@id="modal-51"]/div/div/div[3]/button[1]').click()
    except:
        pass
    get_element(d, 'web_cases.conf',gw_type)
    print('注册完成。。。')
    d.quit()



if __name__ == '__main__':
    host = '172.16.6.165'
    gw_gsm = 'gsm'    # 模拟网关： analog  其他 gsm
    # gw_analog = 'analog'    # 模拟网关： analog  其他 gsm

    manin(host,gw_gsm)
