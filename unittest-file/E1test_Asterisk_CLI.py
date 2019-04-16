#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
************************************
# Author     : Lei YC         
# Created on : 2018/1/2010:59 
# Filename   : E1test_Asterisk_CLI.py
************************************
'''
from selenium import webdriver
import unittest, time
import HTMLTestReportCN
import configparser
class Asterisk_CLI(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.file = './web_cases.conf'
        self.config.read(self.file)
        secs = self.config.sections()
        print("sections:", secs)
        print(self.file)
        self_host = self.config.get('gateway', 'hostname')
        self_gwtype = self.config.get('gateway', 'gw_type')
        cache = self.config.get('test_web_login', 'current')
        cache = cache.split(';')
        self_username = cache[0]
        self_passwd = cache[1]
        self_port = cache[3]
        self_loginmode = cache[4]
        if self_loginmode == 'only https':
            self_port = 443
            self_loginmode = 'https'
        else:
            self_port = 80
            self_loginmode = 'http'
        a = '%s://%s:%s@%s:%s' % (self_loginmode, self_username, self_passwd, self_host, int(self_port))
        print(a)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.url = a
        self.driver.get(self.url)
        self.driver.set_window_size(1024, 768)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="mynav5"]').click()
        self.driver.find_element_by_xpath('//*[@id="qh_con5"]/ul/li[4]').click()
    def tearDown(self):
       self.driver.quit()
    def test1(self):
        '''测试Asterisk 命令接口功能 输入错误的CLI命令 获取输出结果'''
        driver = self.driver
        print(driver.title)
        driver.find_element_by_xpath('//*[@id="command"]').send_keys('sip show peerssdasd')
        driver.find_element_by_css_selector("[type = 'submit']").click()  # 保存按键
        a = driver.find_element_by_xpath('//*[@id="lps"]').text
        file = open('tmp.txt', 'w')
        for i in a:
            file.write(i)
        file.close()
        s = open('tmp.txt')
        c = s.read()
        if 'No such command' in c:
            e = '输入错误asterisk命令测试通过'
            print(e)
        else:
            print('测试失败')
        s.close()
        #driver.find_element_by_id('apply').click()
        self.assertEqual(e, u'输入错误asterisk命令测试通过')
    def test2(self):
        '''测试Asterisk 命令接口功能：输入正确的CLI命令 获取输出结果'''
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="command"]').send_keys('sip show peers')
        driver.find_element_by_css_selector("[type = 'submit']").click()  # 保存按键
        a = driver.find_element_by_xpath('//*[@id="lps"]').text
        file = open('tmp.txt', 'w')
        for i in a:
            file.write(i)
        file.close()
        s = open('tmp.txt')
        c = s.read()
        if 'No such command' in c:
            print()
        else:
            e = '输入asterisk命令测试通过'
            print(e)
        s.close()
        #driver.find_element_by_id('apply').click()
        self.assertEqual(e, u'输入asterisk命令测试通过')
    def test3(self):
        '''测试Asterisk 命令接口功能 锁定/解锁通道 测试前需要先见网关设置为SS7信令'''
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="channelnum"]').send_keys('2')
        driver.find_element_by_xpath('//*[@id="channelcount"]').send_keys('6')
        driver.find_element_by_xpath('//*[@id="lps"]/form/table[2]/tbody/tr[6]/td/input').click()
        a = driver.find_element_by_xpath('//*[@id="lps"]').text
        file = open('tmp.txt', 'w')
        for i in a:
            file.write(i)
        file.close()
        s = open('tmp.txt')
        c = s.read()
        if 'Sending Blocking message to peer' in c:
            e = '测试Asterisk 命令接口功能 锁定/解锁通道'
            print(e)
        else:
            print('cuowu')
        s.close()
        self.assertEqual(e, u'测试Asterisk 命令接口功能 锁定/解锁通道')

if __name__ == '__main__':
#   unittest.main()
    #suite = unittest.TestSuite()
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Asterisk CLI))
    test = unittest.TestSuite()
    #test.addTest(E1test_time("test1_localtime"))
    test.addTest(Asterisk_CLI("test1"))
    test.addTest(Asterisk_CLI("test2"))
    test.addTest(Asterisk_CLI("test3"))
    #test.addTest(E1test("test_cludserver"))
    filename = '.\E1test_Asterisk_CLI.html'
    fp = open(filename, 'wb')
    runner = HTMLTestReportCN.HTMLTestRunner(stream=fp,
                                             title=u'测试Asterisk 命令接口功能',
                                             description=u'测试Asterisk 命令接口功能')

    runner.run(test)
    fp.close()




