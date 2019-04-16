'''
-*- coding: utf-8 -*-
@Author  : Ray Lei
@Time    : 2018/5/3 17:29
@Software: PyCharm
@File    : T_general.py
'''


import unittest,HTMLTestReportCN,configparser,time,socket
import datetime
from selenium import webdriver
import threading
from selenium.webdriver.support.ui import Select
import subprocess as sp


class test_general(unittest.TestCase):
    def setUp(self):
        u'''初始化参数'''
        self.config_file = '../config/web_cases.conf'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.hostname = self.config.get('gateway', 'hostname')
        self.gw_type = self.config.get('gateway', 'gw_type')
        cache = self.config.get('test_web_login', 'current')
        cache = cache.split(';')
        self.username = cache[0]
        self.password = cache[1]
        self.port = cache[3]
        self.baseurl = 'http://%s:%s@%s' % (self.username, self.password, self.hostname)

        self.verificationErrors = []
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1024, 768)
        self.driver.implicitly_wait(5)
        print(self.baseurl)
        self.driver.get(self.baseurl)

    def tearDown(self):
        u'''关闭文件，关闭浏览器'''
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def __sync_client_time(self):
        driver = self.driver
        driver.find_element_by_link_text('Time').click()
        js = 'var q=document.documentElement.scrollTop=100000'
        driver.execute_script(js)
        driver.find_element_by_xpath("//input[@value='Sync from Client']").click()
        time.sleep(1)
        sys_time = driver.find_element_by_xpath('//*[@id="currenttime"]').text
        # print('系统时间：%s' % sys_time)
        return sys_time


    def __get_time(self): 
        TM = datetime.datetime
        sys_time = TM.now().strftime('%Y-%m-%d %H:%M:%S')
        Second = sys_time.split(" ")[1].split(":")[2]
        Day = sys_time.split(" ")[0].split('-')[2]
        if int(Second) > 30:
            '''当物理环境较差时(网络慢，设备反应慢，web界面卡顿等)
            可以将上面的50改小一点，以增加等待验证的时间'''
            reboot_time = (TM.now() + datetime.timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M')
            Hour = reboot_time.split(" ")[1].split(':')[0]
            Minute = reboot_time.split(" ")[1].split(':')[1]
        else:
            reboot_time = (TM.now() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
            Hour = reboot_time.split(" ")[1].split(':')[0]
            Minute = reboot_time.split(" ")[1].split(':')[1]

        week = TM.strptime(sys_time.split(" ")[0], '%Y-%m-%d').weekday()
        w = {'6':0,'5':6, '4':5, '3':4, '2':3, "1":2, "0":1}
        Week = w[str(week)]
        d = {'00':0,'01':1, '02':2, '03':3, '04':4, "05":5, "06":6, "07":7, "08":8, "09":9}
        if Day.startswith('0'):
            Day = d[Day]
        else:
            Day = int(Day)
        if Hour.startswith('0'):
            Hour = d[Hour]
        else:
            Hour = int(Hour)
        if Minute.startswith("0"):
            Minute = d[Minute]
        else:
            Minute = int(Minute)
        # print('Second: %s|reboot_time: %s|Week: %s|Hour: %s|Minute: %s..' % (Second, reboot_time, Week, Hour, Minute))
        # print('reboot time %s' %  reboot_time)
        return Week, Day, Hour, Minute, reboot_time


    def __modify_general_setting(self,is_enable,test_type,Week, Day, Hour, Minute):
        driver = self.driver
        driver.find_element_by_link_text('General').click()
        js = 'var q=document.documentElement.scrollTop=10000'
        driver.execute_script(js)
        time.sleep(0.3)
        reboot_sw = driver.find_element_by_id('reboot_sw')
        s0 = Select(driver.find_element_by_id('reboot_type'))
        if is_enable:
            '''开启定时重启功能'''
            if reboot_sw.get_attribute('checked') == None:
                print('正在开启中')
                driver.find_element_by_xpath('//*[@id="lps"]/form/table[1]/tbody/tr[1]/td/div/div[1]/div/div').click()
                time.sleep(1)
            else:
                print('已开启')
            if test_type == 'day':
                '''需要的元素：Hour，Minute'''
                print('reboot by day')
                s0.select_by_value('by_day')
                driver.find_element_by_xpath('//*[@value="by_day"]').click()
                s1 = Select(driver.find_element_by_xpath('//*[@id="d_hour"]'))
                s2 = Select(driver.find_element_by_xpath('//*[@id="d_minute"]'))
                s1.select_by_value('%s' % Hour)
                s2.select_by_value('%s' % Minute)

            elif test_type == 'week':
                '''需要的元素：week，hour，minus'''
                print('reboot by week')
                s0.select_by_value('by_week')
                s1 = Select(driver.find_element_by_xpath('//*[@id="w_hour"]'))
                s2 = Select(driver.find_element_by_xpath('//*[@id="w_minute"]'))
                s3 = Select(driver.find_element_by_xpath('//*[@id="w_week"]'))
                s1.select_by_value('%s' % Hour)
                s2.select_by_value('%s' % Minute)
                s3.select_by_value('%s' % Week)

            elif test_type == "month":
                '''需要的元素：day，hour，minus'''
                print('reboot by month')
                s0.select_by_value('by_month')
                # driver.find_element_by_xpath('//*[@value="by_month"]').click()
                s1 = Select(driver.find_element_by_xpath('//*[@id="m_hour"]'))
                s2 = Select(driver.find_element_by_xpath('//*[@id="m_minute"]'))
                s3 = Select(driver.find_element_by_xpath('//*[@id="m_month"]'))
                driver.find_element_by_xpath('//*[@id="m_month"]/option[%s]' % Day).click()
                s1.select_by_value('%s' % Hour)
                s2.select_by_value('%s' % Minute)
                s3.select_by_value('%s' % Day)

            elif test_type == "running_time":
                pass

            elif test_type == "False":
                print('定时重启关闭')
                if reboot_sw.get_attribute('checked') == None:
                    pass
                else:
                    print('正在关闭')
                    driver.find_element_by_xpath('//*[@id="lps"]/form/table[1]/tbody/tr[1]/td/div/div[1]/div/div').click()               
                s0.select_by_value('by_day')
                driver.find_element_by_xpath('//*[@value="by_day"]').click()
                s1 = Select(driver.find_element_by_xpath('//*[@id="d_hour"]'))
                s2 = Select(driver.find_element_by_xpath('//*[@id="d_minute"]'))
                s1.select_by_value('%s' % Hour)
                s2.select_by_value('%s' % Minute)

        js = 'var q=document.documentElement.scrollTop=10000'
        driver.execute_script(js)
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@value="Save"]').click()
        except:
            print('没有保存')
        else:
            print("保存成功")

        time.sleep(1)

        try:
            driver.find_element_by_id('apply').click()

        except:
            print('无法加载配置 reboot设置失败')
            driver.save_screenshot('pictures/test_Scheduled_Reboot_by_%s.png ' % (test_type))
            driver.quit()
            return False
        else:
            time.sleep(1)
            print('加载成功')
            driver.quit()
            return True


    def __verify_general_setting(self,reboot_time,reboot_type):
        ip = self.hostname
        R_T = reboot_time + ':00'
        rt = time.strptime(R_T, '%Y-%m-%d %H:%M:%S')
        rt_timeStamp = int(time.mktime(rt))
        L_T = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        lt_now = time.strptime(L_T, '%Y-%m-%d %H:%M:%S')
        lt_timeStamp = int(time.mktime(lt_now))
        w_t = int(rt_timeStamp - lt_timeStamp)
        print('重启时间%s -- 当前时间%s' % (R_T,L_T))
        print('即将开始重启.............\n%s 秒后开始验证重启是否生效' % w_t)
        time.sleep(w_t+10)
        '''为了保证获取到正确的状态信息，
        可以对等待时间进行调整'''
        print('开始验证..',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        status, result = sp.getstatusoutput("ping " + ip + " -w 2000")
        if reboot_type == 'False':
            print('测试关闭自动重启功能')
            print('%s 可以访问' % ip)
            return False
            # print('False')
        elif "请求超时" in result:
            print('%s 无法访问' % ip)
            # print(status,result)
            return False
            # print('False')
        else:
            print('%s 可以访问' % ip)
            return True
            # print('True')

    def web_general_case(self,reboot_type):
        '''定义 general 测试用例集'''
        self.__sync_client_time()
        get_time = self.__get_time()
        info = self.__modify_general_setting(True,reboot_type,get_time[0],get_time[1],get_time[2],get_time[3])
        if info == True:
            time.sleep(0.5)
            self.assertFalse(self.__verify_general_setting(get_time[4],reboot_type),
                            msg = "Error reboot by %s failed!!!\ngateway should be reboot but it's still Connectable." % reboot_type)
        else:
            self.assertTrue(False, msg = 'Input error,Failed to load configuration...\nreboot by %s setting failed' % reboot_type)
        print('设备正在重启中，请耐心等待')
        time.sleep(40)

    @staticmethod
    def get_testcase(reboot_type):
        def func(self):
            u'''general 测试用例'''
            print('testcases_type: ',reboot_type)
            self.web_general_case(reboot_type)
        return func

def __generate_testcases():
    config_file = '../config/web_cases.conf'
    config = configparser.ConfigParser()
    config.read(config_file)
    arglists = []
    testcases = config.get('test_general', 'testcases')
    testcases = testcases.split(';')
    print(list(testcases))
    for test in testcases:
        args = config.get('test_general', test).split(';')
        print(args)
        setattr(test_general, 'test_general_%s' % test, test_general.get_testcase(*args))

if __name__ == '__main__':
    # for i in range(10):
    #     print('-----这是第%s次运行-----' % (int(i)+1))
    __generate_testcases()
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_general))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    time.sleep(10)

    # fp = open('general.html', 'wb')
    # runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title='Report_title', description='Report_description')
    # runner.run(suite)
    # fp.close()


else:
    __generate_testcases()