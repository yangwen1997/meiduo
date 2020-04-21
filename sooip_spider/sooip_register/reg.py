import re
import os
import time
import redis

from PIL import Image
from selenium import webdriver

from custom.lib_utils import get_userNameAndPassword, md5
from custom.register_libs.ruokuai import RClient, LAE_5
from custom.register_libs.mayi import SmsGetter




def get_img_catalogue():
    """
    :return: 返回路径
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    raw_img_path = os.path.join(dir_path, 'raw.png')
    now_img_path = os.path.join(dir_path, 'now.png')
    return raw_img_path, now_img_path


TEST_PHONE = 18328021878


class Register:
    def __init__(self, raw, now, proxy=None):
        self.reg_url = 'http://www.sooip.com.cn/app/userRegistration'
        self.proxy = proxy
        self.raw_img = raw
        self.now_img = now
        self.rk = RClient()
        self.sms = SmsGetter(ID=14141, digit=6)
        self.redis_client = redis.Redis(host='10.2.1.91', port=6379, db=4)
        self.__init__driver()

    def __init__driver(self):
        if self.proxy:
            chromeOptions = webdriver.ChromeOptions()
            proxy_param = "--proxy-server=http://{proxy}".format(proxy=self.proxy)
            chromeOptions.add_argument(proxy_param)
            self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        else:
            self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def main(self):
        while 1:
            self.driver.get(self.reg_url)
            usr, psd = get_userNameAndPassword()
            self.register(usr, psd)

    def get_phone(self):
        phone = self.sms.getMobile()
        regex = re.compile('^1[3|4|5|7|8][0-9]{9}$')
        if regex.match(phone):
            return phone
        else:
            print('手机号码无效，重试中')
            return self.get_phone()

    def get_sms(self, phone):
        for i in range(1, 4):
            time.sleep(i*10)
            sms_code = self.sms.getCode(phone)
            if sms_code:
                return sms_code

    def register(self, usr, psd):
        self.driver.find_element_by_id('login_id').send_keys(usr)
        self.driver.find_element_by_id('login_pwd').send_keys(psd)
        self.driver.find_element_by_id('login_pwd_conf').send_keys(psd)
        self.driver.find_element_by_id('regi_btn1').click()
        time.sleep(1)
        self.screen_img()
        yzm_code, yzm_id = self.identify_code()
        self.driver.find_element_by_id('cert_code1').send_keys(yzm_code)
        e_mail_input = self.driver.find_element_by_id('e_mail')
        e_mail_input.send_keys(TEST_PHONE)
        time.sleep(1)
        if self.catch_error():
            self.rk.rk_report_error(yzm_id)
            return None
        else:
            e_mail_input.clear()
            phone = self.get_phone()
            e_mail_input.send_keys(phone)
            self.driver.find_element_by_id('sendEmail').click()
            sms_code = self.get_sms(phone)
            if sms_code:
                self.driver.find_element_by_id('cert_code').send_keys(sms_code)
                self.driver.find_element_by_id('regiestReq').click()
                time.sleep(2)
                self.is_logged(usr, psd)

    def is_logged(self, usr, psd):
        if self.driver.current_url == 'http://www.sooip.com.cn/app/userMain':
            write_account(usr, psd)
            self.save_cookie(usr, psd)

    def save_cookie(self, usr, psd):
        cookie = self.handle_cookie()
        account_key = 'account:sooip:{0}'.format(usr)
        cookie_key = 'cookies:sooip:{0}'.format(usr)
        self.redis_client.set(account_key, psd)
        self.redis_client.set(cookie_key, cookie)
        print('存储到redis成功')

    def handle_cookie(self):
        cookie = {}
        for i in self.driver.get_cookies():
            cookie[i["name"]] = i["value"]
        return cookie

    def catch_error(self):
        if self.driver.find_element_by_id('login_codelabel1_error').text == '验证码错误':
            return True
        return False

    def identify_code(self):
        im = open('now.png', 'rb').read()
        res = self.rk.rk_create(im, LAE_5)
        return res['Result'], res['Id']

    def screen_img(self):
        print('------------截图开始------------')
        self.driver.get_screenshot_as_file(self.raw_img)
        rangle = (1205, 383, 1326, 425)
        i = Image.open(self.raw_img)
        frame4 = i.crop(rangle)
        frame4.save(self.now_img)
        print('--------------截图完毕-----------')
        time.sleep(0.5)


def write_account(usr, psd):
    with open('account.txt', 'a+') as f:
        print('注册成功', usr)
        f.write(usr + '  ' + psd+'\n')


if __name__ == '__main__':
    raw, now = get_img_catalogue()
    logger = Register(raw, now, '10.0.0.50:9999')
    logger.main()