import os
from numpy import arange
import random
import time
import re
from functools import reduce
from io import BytesIO
import requests
import logging as log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from register_spider import RegisterSpider


class RegisterUserSpider(object):
    def __init__(self, ID):
        # 天眼查网站蚂蚁验证码平台项目ID
        self.ID = ID

    # 主程序入口
    def run(self):
        register = RegisterSpider(log=log, project_id=self.ID)
        # 验证账号获取token
        token = register.check_use()
        if token:
            for _ in range(1000):
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
        chrome_options.add_argument("--proxy-server=http://10.0.0.54:9999")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-infobars')
        # chrome_options.add_argument("--proxy-server=http://10.0.0.50:9999")
        path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)

        url = "https://www.tianyancha.com/login"
        driver.get(url)
        time.sleep(1)

        # 点击免费注册按键
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[@class='text-center pt28']/div")))
            element.click()
        except Exception:
            log.error('点击免费注册失败')
        time.sleep(0.3)
        # # 验证是否跳转
        # try:
        #     element = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[1]"), '免费注册'))
        # except Exception:
        #     log.error('找不到免费注册这个元素')

        # 添加手机号码
        try:
            # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[2]/input")))
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[2]/input")))
            element.send_keys(cell)
        except Exception:
            log.error('找不到添加手机号的元素')


        # 点击获取验证码
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[3]/div")))
            # time.sleep(0.5)
            element.click()
            time.sleep(0.5)
            element.click()
        except Exception:
            log.error('找不到获取验证码的元素')
        time.sleep(3)
        try:
            element.click()
        except Exception:
            pass

        # 验证码处理
        try:
            self.image_handle(driver)
        except Exception as e:
            log.error(e)

        # 检查账号是否被注册过
        try:
            element = WebDriverWait(driver, 2).until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[2]/div"),'手机号己注册，请直接登录'))
            if element:
                driver.quit()
                return
        except Exception:
            log.error('找不到验证账号是否注册提示的元素')

        time.sleep(10)
        # 获取验证码
        for _ in range(3):
            code_content = register.get_code(cell, token, ID)
            if code_content:
                break
            else:
                log.info('sleep 10s')
                time.sleep(10)

        if code_content:
            # 从短信模板解析验证码
            try:
                code = re.search('验证码是：(\d+)，', str(code_content)).group(1)
            except Exception:
                code = None
            log.info(code)
            # 填写验证码
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[3]/input")))
                element.send_keys(code)
            except Exception:
                log.error('找不到填写验证码的元素')
            # 填写密码
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[5]/input")))
                element.send_keys('a123456789')
            except Exception:
                log.error('找不到填写密码的元素')
            # 确认密码
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[6]/input")))
                element.send_keys('a123456789')
            except Exception:
                log.error('找不到确认密码的元素')
            # 点击注册
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='module module3 registermodule register_box pl30 pr30 collapse in']/div[7]")))
                element.click()
                time.sleep(1)
                dic = {
                    'use': int(cell),
                    'password': 'a123456789',
                    'flag': True ,
                    'status': 0,
                }
                register.insert_account('tyc_account_results', dic)
            except Exception:
                log.error('找不到确认密码的元素')
            driver.quit()
        else:
            driver.quit()
    # 验证码处理
    def image_handle(self, driver):
        img_url1, img_url2 = self.drag_pic(driver)
        # print(img_url1)
        offset = crack_picture(img_url1, img_url2).pictures_recover()
        tsb = self.emulate_track(driver,offset)
        # print(tsb)

    def drag_pic(self, driver):
        return (self.find_img_url(self.wait_for(driver, By.CLASS_NAME, "gt_cut_fullbg_slice")),
                self.find_img_url(self.wait_for(driver, By.CLASS_NAME, "gt_cut_bg_slice")))

    def wait_for(self, driver, by1, by2):
        return WebDriverWait(driver, 5).until(EC.presence_of_element_located((by1, by2)))

    def find_img_url(self, element):
        try:
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")

    def emulate_track(self, driver, offset):
        element = driver.find_element_by_class_name("gt_slider_knob")
        easings = easing()
        offsets, tracks = easings.get_tracks(offset, 12)
        ActionChains(driver).click_and_hold(element).perform()
        for x in tracks:
            ActionChains(driver).move_by_offset(x, 0).perform()
        ActionChains(driver).pause(0.5).release().perform()

# 验证码处理类
class crack_picture(object):
    def __init__(self, img_url1, img_url2):
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)

    def picture_get(self, img_url1, img_url2):
        hd = {"Host": "static.geetest.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        img1 = BytesIO(self.repeat(img_url1, hd).content)
        img2 = BytesIO(self.repeat(img_url2, hd).content)
        return img1, img2

    def repeat(self, url, hd):
        times = 10
        while times > 0:
            try:
                ans = requests.get(url, headers=hd)
                return ans
            except:
                times -= 1

    def pictures_recover(self):
        xpos = self.judge(self.picture_recover(self.img1, 'img1.jpg'),
                          self.picture_recover(self.img2, 'img2.jpg')) - 6
        return xpos

    def picture_recover(self, img, name):
        a = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43,
             42, 12,13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):
                right = a[row * 26 + column] % 26 * 12 + 1
                down = 58 if a[row * 26 + column] > 25 else 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new

    def judge(self, img1, img2):
        for i in range(img2.size[0]):
            if self.col(img1, img2, i):
                return i
        return -1

    def diff(self, img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp = reduce(lambda x, y: x + y, map(lambda x: abs(x[0] - x[1]), zip(rgb1, rgb2)))
        return True if tmp >= 200 else False

    def col(self, img1, img2, cl):
        for i in range(img2.size[1]):
            if self.diff(img1, img2, cl, i):
                return True
        return False


class easing(object):

    def ease_out_quad(self, x):
        return 1 - (1 - x) * (1 - x)

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def ease_out_expo(self, x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    def get_tracks(self, distance, seconds):
        tracks = [0]
        offsets = [0]
        r = random.randint(1, 3)
        for t in arange(0.0, seconds, 0.1):
            if r == 1:
                offset = round(self.ease_out_quad(t / seconds) * distance)
            elif r == 2:
                offset = round(self.ease_out_expo(t / seconds) * distance)
            else:
                offset = round(self.ease_out_quart(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        return offsets, tracks

if __name__=='__main__':
    realpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/log/"
    filename = "{}_register_debug_{}.log".format(realpath, time.strftime("%Y-%m-%d", time.localtime()))

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

    base = RegisterUserSpider('6022')
    base.run()