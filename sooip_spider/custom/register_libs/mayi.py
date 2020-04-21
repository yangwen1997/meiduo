import re
import time

import requests


class SmsGetter:
    def __init__(self, ID, digit=4, username='whitedgg', password='dgg123456'):
        self.username = username
        self.password = password
        self.digit = digit
        self.ID = ID
        self.login()

    def login(self):
        url = "http://www.66yzm.com/api/admin/dengl?zhanghao={0}&mima={1}".format(self.username, self.password)
        try:
            res = requests.get(url).text
            dic = eval(res)
            token = dic["token"]
            self.token = token
        except Exception as e:
            print(e)
            self.token = None
            raise Exception('登陆失败')

    # 获取手机号
    def getMobile(self):
        # 获取真实号段链接
        url = "http://www.66yzm.com/api/admin/getmobile?linpai={}&itemid={}&xunihaoduan=1".format(self.token, self.ID)
        # 获取虚拟号段链接
        # url = "http://www.66yzm.com/api/admin/getmobile?linpai={0}&itemid={1}&xunihaoduan=1".format(token, itemId)
        try:
            res = requests.get(url).text
            number = re.findall("(1[0-9]{10})", res)[0]
            print(number)
            return number
        except:
            return "null"


    # 获取验证码
    def getCode(self, number):
        url = "http://www.66yzm.com/api/admin/shortmessage?linpai={0}&itemid={1}&mobile={2}".format(self.token,
                                                                                                    self.ID, number)
        try:
            res = requests.get(url).text
            # 正则匹配验证码，根据验证码位数修改花括号中的数字即可
            code = re.findall("([0-9]{%s})"%self.digit, res)[0]
            print(code)
            return code
        except:
            return None

    # 拉黑手机号
    def blackNumber(self, number):
        url = "http://www.66yzm.com/api/admin/blacklist?linpai={0}&itemid={1}&mobile={2}".format(self.token, self.ID, number)
        requests.get(url)


if __name__ == '__main__':
    a = SmsGetter(ID=14141, digit=6)
    num = a.getMobile()
    time.sleep(40)
    a.getCode(num)
    a.blackNumber(num)
