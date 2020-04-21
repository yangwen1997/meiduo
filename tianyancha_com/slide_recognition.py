from numpy import arange
import random
import re
from functools import reduce
from io import BytesIO
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

class SlideRecognition(object):
    # 滑块验证码处理
    def image_handle(self, driver):

        img_url1, img_url2 = self.drag_pic(driver)
        # print(img_url1)
        offset = crack_picture(img_url1, img_url2).pictures_recover()
        self.emulate_track(driver, offset)


    def drag_pic(self, driver):
        return (self.find_img_url(self.wait_for(driver, By.CLASS_NAME, "gt_cut_fullbg_slice")),
                self.find_img_url(self.wait_for(driver, By.CLASS_NAME, "gt_cut_bg_slice")))

    def wait_for(self, driver, by1, by2):
        return WebDriverWait(driver, 5).until(EC.presence_of_element_located((by1, by2)))

    def find_img_url(self, element):
        try:
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg").replace("https",'http')
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg").replace("https",'http')

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
             42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
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

# 缓动函数类处理
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