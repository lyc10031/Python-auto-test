#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 11:26
# @Author  : ray lei
# @File    : smsbank.py
# @Software: PyCharm


from collections import Counter
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Modify_GW_Line_number(object):
    """
    docstring for Modify_GW_Line_number
    修改网关 注册端口数量。
    """

    def __init__(self, ip, gw_name, port_num):
        """
        ip:simbank IP地址
        gw_name:网关序列号
        port_num:注册端口数量
        """
        self.d = webdriver.Firefox()
        self.gw_name = gw_name
        self.port_num = port_num
        url_web = 'http://admin:admin@' + ip
        self.d.set_window_size(1024, 768)
        self.d.get(url_web)
        time.sleep(1)

    def Simbank_Register(self):

        '''Register_gateway '''
        d = self.d
        d.find_element_by_link_text('REGISTER').click()
        gw_ele = d.find_element_by_xpath(
            "//*[contains(text(),'%s')]/.." % self.gw_name)  # 定位到网关序列号。
        gw_ele.find_element_by_css_selector(
            "td:nth-child(9) > button:nth-child(1)").click()  # 点击modify。
        try:
            self.Modify_GW_onLine_number(self.gw_name)
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            self.d.find_element_by_link_text('REGISTER').click()

    def Modify_GW_onLine_number(self, gw_name):
        '''修改端口数量 '''
        d = self.d
        port = self.port_num
        old_num = d.find_element_by_xpath(
            '//*[@id="n_gw_links"]').get_attribute('value')  # 获取原有端口数量
        new_list = [str(i) for i in range(1, port+1) if i != int(old_num)]
        new_num = random.choice(new_list)
        d.find_element_by_id('n_gw_links').clear()
        d.find_element_by_id('n_gw_links').send_keys(new_num)
        # time.sleep(0.5)
        d.find_element_by_css_selector("[type = 'submit']").click()
        print(
            f"The Gateway: * {gw_name} *  registered to Simbank's port changed from {old_num} to {new_num} .....")


    def main(self):
        self.Simbank_Register()
        # print('change_GW_On_Line_number OK...')
        # print(f"The Gateway: * {self.gw_name} *  registered to Simbank's port changed from {old_num} to {new_num} .....")
        # self.d.close()
    def __del__(self):
        self.d.close()

if __name__ == "__main__":
    ip = '172.16.6.169'
    # gw_list = ['TACQUYKC','TACQULA5']
    gw_list = ['TACQUEAG', '4BGDMAMV']
    # gw = 'TACQULA5'

    """ 
	1、ip:simbank ip 
	2、gw: 网关序列号
	3、网关端口数量
	"""
    # run = Modify_GW_Line_number(ip, gw, 32)
    # run.main()

    [Modify_GW_Line_number(ip, gw, 32).main() for gw in gw_list]
    print('change_GW_On_Line_number OK...')

    