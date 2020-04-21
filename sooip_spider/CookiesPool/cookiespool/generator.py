import hashlib
import json
import random
import re

import requests
from config import *
from cookiespool.db import CookiesRedisClient, AccountRedisClient



class CookiesGenerator(object):
    def __init__(self, name='default'):
        self.name = name
        self.cookies_db = CookiesRedisClient(name=self.name)
        self.account_db = AccountRedisClient(name=self.name)

    def new_cookies(self, username, password):
        raise NotImplementedError

    def set_cookies(self, account):
        """
        cookies写入redis
        :param account: 账号信息
        :return:
        """
        results = self.new_cookies(account.get('username'), account.get('password'))
        if results:
            username, cookies = results
            print('Saving Cookies to Redis', username, cookies)
            self.cookies_db.set(username, cookies)

    def run(self):
        accounts = self.account_db.all()
        cookies = self.cookies_db.all()
        accounts = list(accounts)
        valid_users = [cookie.get('username') for cookie in cookies]
        print('Getting', len(accounts), 'accounts from Redis')
        for account in accounts:
            if not account.get('username') in valid_users:
                print('Getting Cookies of ', self.name, account.get('username'), account.get('password'))
                self.set_cookies(account)
        print('Generator Run Finished')

PROXY_LIST = ['10.0.0.50:9999', '10.0.0.53:9999', '10.0.0.55:9999']


class SooipCookiesGenerator(CookiesGenerator):
    """
    sooip网站cookie维护
    """
    def __init__(self, name='sooip'):
        CookiesGenerator.__init__(self, name)
        self.name = name
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

    def new_cookies(self, username, password):
        """
        登陆生成心得cookies
        :param username:用户名
        :param password: 密码
        :return:
        """
        print('Generating Cookies of', username)
        proxy = random.choice(PROXY_LIST)
        post_url = "http://www.sooip.com.cn/txn999999.ajax"
        data = {'username': username, 'password': hashlib.md5(password.encode('utf8')).hexdigest().upper()}
        proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
        resp = requests.post(post_url, headers=self.headers, data=data, proxies=proxies)
        cookies = resp.cookies.get_dict()
        if self.is_success(resp):
            return (username, json.dumps(cookies))

    def is_success(self, resp):
        """
        判断是否登陆成功
        :param resp:
        :return:
        """
        flag = re.search('<error-code>000000</error-code>', resp.text)
        if flag:
            return True
        else:
            return False


class CniprCookiesGenerator(CookiesGenerator):
    def __init__(self, name='cnipr'):
        CookiesGenerator.__init__(self, name)
        self.name = name
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

    def new_cookies(self, username, password):
        print('Generating Cookies of', username)
        post_url1 = "http://search.cnipr.com/login.action?rd={0}".format(random.uniform(0, 1))
        post_url2 = "http://search.cnipr.com/login!goonlogin.action?rd={0}".format(random.uniform(0, 1))

        #第一次登陆
        resp = self.login(post_url1, username, password)
        if self.is_success(resp) == 'success':
            cookies = resp.cookies.get_dict()
            return (username, json.dumps(cookies))
        #第二次登陆
        elif self.is_success(resp) == 'alreadylogin':
            resp2 = self.login(post_url2, username, password)
            if self.is_success(resp2) == 'success':
                cookies = resp2.cookies.get_dict()
                return (username, json.dumps(cookies))

    def login(self, post_url, username, password):
        proxy = random.choice(PROXY_LIST)
        proxies = {'http': 'http://' + proxy}
        data = {'username': username, 'password': password}
        resp = requests.post(post_url, headers=self.headers, data=data, proxies=proxies)
        return resp

    def is_success(self, resp):
        if resp.json()['msg'] == 'success':
            return 'success'
        elif resp.json()['msg'] == 'alreadylogin':
            return 'alreadylogin'
        return False


if __name__ == '__main__':
    qi = SooipCookiesGenerator()
    qi.new_cookies('kFJIc176', 'coTUsTL')
    pass
