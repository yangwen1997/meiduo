#!/usr/bin/env python
# coding:utf-8
from enum import Enum, unique
import requests
from hashlib import md5


#3040  4位数字和英文  |  3050  5位数字和英文

LAE_4 = 3040
LAE_5 = 3050

username = 'brantzxj'
password = 'dgg123456'
soft_id = '108559'
soft_key = '438362e5d4454a2c92db4ad847463b7a'


class RClient(object):
    def __init__(self, username=username, password=password,
                 soft_id=soft_id, soft_key=soft_key):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', headers=self.headers, data=params, proxies={'http': 'http://10.0.0.50:9999'}, files=files, )
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    rc = RClient()
    im = open('val.png', 'rb').read()
    click_str = rc.rk_create(im, LAE_4)
    print(click_str)



