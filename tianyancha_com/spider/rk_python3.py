#!/usr/bin/env python
# coding:utf-8

import requests
import hashlib

class RClient(object):
    '''
    验证码接口文档
    '''
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = hashlib.md5(password.encode("utf-8")).hexdigest()
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

    def rk_create(self, data,im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': (data, im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers).json()
        # return r.json()
        # print("[INFO]: 返回的接口数据为{}".format(r))
        return r

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        print("[INFO]: 打码错误信息已经返回平台")
        return r.json()


def identify(data):
    print("[INFO]: 传输过来的文件名称{}".format(data))
    rc = RClient('brantzxj', 'dgg123456', '106510', '62876ef380f94e029513c048727e2208')
    im = open(data, 'rb').read()
    click_str = rc.rk_create(data,im, 6900)
    return click_str

def error_id(id_info):
    print("[INFO]: 传输过来的文件id：{}".format(id_info))
    rc = RClient('brantzxj', 'dgg123456', '106510', '62876ef380f94e029513c048727e2208')
    click_str = rc.rk_report_error(id_info)
    return click_str
