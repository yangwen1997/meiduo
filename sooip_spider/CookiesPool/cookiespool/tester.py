import re
import random
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *

PROXY_LIST = ['10.0.0.50:9999', '10.0.0.53:9999', '10.0.0.54:9999', '10.0.0.55:9999']


class ValidTester(object):
    def __init__(self, name='default'):
        self.name = name
        self.cookies_db = CookiesRedisClient(name=self.name)
        self.account_db = AccountRedisClient(name=self.name)

    def test(self, account, cookies):
        raise NotImplementedError

    def run(self):
        accounts = self.cookies_db.all()
        for account in accounts:
            username = account.get('username')
            cookies = self.cookies_db.get(username)
            self.test(account, cookies)


class CniprValidTester(ValidTester):
    def __init__(self, name='cnipr'):
        ValidTester.__init__(self, name)

    def test(self, account, cookies):
        proxies = {'http': 'http://' + random.choice(PROXY_LIST)}
        print('Testing Account', account.get('username'))
        try:
            cookies = eval(cookies)
        except TypeError:
            # Cookie 格式不正确
            print('Invalid Cookies Value', account.get('username'))
            self.cookies_db.delete(account.get('username'))
            print('Deleted User', account.get('username'))
            return None
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
            response = requests.get('http://search.cnipr.com/user!initPage4ModUserInfo.action', headers=headers, cookies=cookies, proxies=proxies)

            if response.status_code == 200:
                if re.search('修改个人信息', response.text):
                    print('Valid Cookies', account.get('username'))
                else:
                    # Cookie已失效
                    print('Invalid Cookies', account.get('username'))
                    self.cookies_db.delete(account.get('username'))
                    print('Deleted User', account.get('username'))
        except ConnectionError as e:
            print('Error', e.args)
            print('Invalid Cookies', account.get('username'))


class SooipValidTester(ValidTester):
    def __init__(self, name='cnipr'):
        ValidTester.__init__(self, name)

    def test(self, account, cookies):
        proxies = {'http': 'http://' + random.choice(PROXY_LIST)}
        print(proxies)
        print('Testing Account', account.get('username'))
        try:
            cookies = eval(cookies)
        except TypeError:
            # Cookie 格式不正确
            print('Invalid Cookies Value', account.get('username'))
            self.cookies_db.delete(account.get('username'))
            print('Deleted User', account.get('username'))
            return None
        try:
            url = 'http://www.sooip.com.cn/app/authorization?pid=PIDUSB12002061100000000006403115711M5320141B6'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
            response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)

            if response.status_code == 200:
                if not re.search('访问无效！', response.text):
                    print('Valid Cookies', account.get('username'))
                else:
                    # Cookie已失效
                    print('Invalid Cookies', account.get('username'))
                    self.cookies_db.delete(account.get('username'))
                    print('Deleted User', account.get('username'))
        except ConnectionError as e:
            print('Error', e.args)
            print('Invalid Cookies', account.get('username'))


if __name__ == '__main__':
    tester = CniprValidTester()
    tester.run()
