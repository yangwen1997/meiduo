import os
import time
import re
import requests
import logging as log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from register_spider import RegisterSpider


class RegisterUserSpider(object):
    def __init__(self, ID):
        # 启信宝网站蚂蚁验证码平台项目ID
        self.ID = ID

    # 主程序入口
    def run(self):
        register = RegisterSpider(log=log, project_id=self.ID)
        # 验证账号获取token
        token = register.check_use()
        if token:
            for _ in range(100):
                # 获取电话
                cell = register.get_cell(token, self.ID)
                if cell:
                    # 注册账号
                    self.register_detail(register, cell, token, self.ID)
                else:
                    # 获取电话失败，重新获取
                    time.sleep(10)
                    continue
                # 注册完成后释放掉该号码
                url = "http://www.66yzm.com/api/admin/releaseadd?linpai={}".format(token)
                res = requests.get(url)

    # 注册
    def register_detail(self, register, cell, token, ID):
        # selenium配置
        chrome_options = Options()
        chrome_options.add_argument("--proxy-server=http://1.29.109.104:9999")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-infobars')
        # chrome_options.add_argument("--proxy-server=http://10.0.0.53:9999")
        path = r'C:\Users\XIII-UP\AppData\Local\Google\Chrome\Application\chromedriver'
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)

        url = "https://www.qichacha.com/user_register"
        driver.get(url)
        time.sleep(1)

        # 添加手机号码
        try:
            # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[2]/input")))
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "phone")))
            element.send_keys(cell)
        except Exception:
            log.error('找不到添加手机号的元素')
        # 检查验证是否通过
        try:
            element = WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='nc_1__scale_text']/span/b"), '验证通过'))
        except Exception:
            log.error('找不到验证通过的元素')
        time.sleep(1)
        # 点击获取验证码
        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[@class='text-primary vcode-btn get-mobile-code']")))
            element.click()
        except Exception:
            log.error('找不到获取验证码的元素')
        time.sleep(10)

        # 获取验证码
        for _ in range(5):
            code_content = register.get_code(cell, token, ID)
            if code_content:
                break
            else:
                log.info('sleep 10s')
                time.sleep(10)

        if code_content:
            # 从短信模板解析验证码
            try:
                code = re.search('验证码是(\d+)。', str(code_content)).group(1)
            except Exception:
                code = None
            log.info(code)
            # 填写验证码
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vcodeNormal")))
                element.send_keys(code)
            except Exception:
                log.error('找不到填写验证码的元素')
            # 填写密码
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pswd")))
                element.send_keys('a123456789')
            except Exception:
                log.error('找不到填写密码的元素')
            # 点击注册
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "register_btn")))
                element.click()
                time.sleep(2)
                dic = {
                    'use': cell,
                    'password': 'a123456789',
                    'flag': True ,
                    'status': 0,
                }
                # 启信宝账号入库
                register.insert_account('qcc_account_results', dic)
            except Exception:
                log.error('找不到确认密码的元素')
        driver.quit()


if __name__=='__main__':
    realpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/log/"
    filename = "{}qichacha_register_debug_{}.log".format(realpath, time.strftime("%Y-%m-%d", time.localtime()))

    log.basicConfig(
        level=log.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y %H:%M:%S',
        filename=filename,
        filemode='w'
    )
    console = log.StreamHandler()
    console.setLevel(log.INFO)
    formatter = log.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    log.getLogger('').addHandler(console)

    base = RegisterUserSpider('6676')
    base.run()