import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from itertools import chain

class Simbank_set_num():
    def __init__(self, ip, SB_name,start_port,*args):
        """
        IP: Simbank IP 地址
        SB_name: 注册的simbank序列号
        start_port: 要写入号码的端口的 起始端口编号
        *args: 号码列表  
        """
        self.ip = ip
        self.SB_name = SB_name
        self.start_port = start_port
        self.port_num = list(chain(*args))  #合并多个list
        self.d = webdriver.Firefox()
        self.d.set_window_size(1024, 768)
        url = 'http://admin:admin@' + ip
        self.d.get(url)
        time.sleep(1)

    def web_set_num(self):
        d = self.d
        num_l = self.port_num
        start_port = int(self.start_port)
        # SM = d.find_element_by_css_selector('.div_tab_title')
        # local_SM_name = SM.get_attribute('value')
        # if local_SM_name != self.SB_name:
        #     Select(SM).select_by_value(self.SB_name)
        # else:
        #     pass
        for i, j in zip(range(start_port, start_port+len(num_l)+1), num_l):
            # d.find_element_by_id(self.SB_name).click()      #1.0.6以前版本

            # SM = Select(d.find_element_by_css_selector('.div_tab_title'))
            # SM.select_by_value(self.SB_name)    #1.0.8版本

            # time.sleep(0.5)
            SM = d.find_element_by_css_selector('.div_tab_title')
            local_SM_name = SM.get_attribute('value')
            if local_SM_name != self.SB_name:
                Select(SM).select_by_value(self.SB_name)
            else:
                pass
            time.sleep(1)

            ele = self.SB_name + '_' + str(i)
            try:
                d.find_element_by_xpath('//*[@id="%s"]' % ele).click()
                d.find_element_by_name('phone_num').send_keys(j)
                d.find_element_by_class_name('edit_save').click()
            except Exception as e:
                print('ERROR...', e)
            print(ele, '  ', j, 'ok..')
            time.sleep(1)

    def main(self):
        self.web_set_num()
        print('Number setting completed...')
        time.sleep(1)
        self.d.quit()


if __name__ == "__main__":
    ip = '172.16.6.169'
    SB = 'TACQ2AJL'
    SB1 = 'GHAZWBOO'
    SB2 = 'TACQ2AAB'

    num_l1 = ['18025346952','18026993173','18002543197','18002544207','18026997363','18026996770','18026998539','18026997059']

    # num_l2 = ['66401','66403','66405','66406','66407','66408','66409','66410']

    # num_l3 = ['66412','66413','66414','66415','66418','66420','66421','66422']


#     num_l5 = ['18002540341', '18002548493', '18002546423','18025317089', '18025334035', '18002547641' ,'18002541949', '18025401526']
# # 
#     num_l6 = ['18018762463', '18018753460','18018708335','18025341229','18002537520','18002583940','18002518361','18002506436']

    f = Simbank_set_num(ip, SB,3, num_l1[2:])
    f.main()


