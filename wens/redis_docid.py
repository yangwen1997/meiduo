'''
@author: 杨文龙
@file : run.py
@time: 2019/5/29
@desc:
'''

# 基本模块
import re
import json

# 调式
from random import choice

import execjs
import hashlib
import gc
import requests
from fake_useragent import UserAgent
from easydict import EasyDict

# 本地
from wens.feach import FEACH
from wens.common import get_proxy, URI, DESCENDING, COLLECTION, REDIS,get_log
from wens.docid import decrypt_doc_id
from wens.docid_key import parse_run_eval
from wens.mongo import MongoDB
from wens.dl_js.args import *
from wens.get_ip import GetIP

# 全局配置
log = get_log()
# mongdo
DB = MongoDB(uri=URI, db=DESCENDING, collection=COLLECTION)
red_cli = REDIS

ua = UserAgent()


class WENS(object):
    """
    裁判文书类
    """

    def __init__(self, search):
        """
        初始化
        """
        self.f = FEACH()
        self.url = 'http://wenshu.court.gov.cn/'
        self.proxy = None
        self.search = search

    def request_list(self,index:int):
        """请求列表数据"""
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        })
        vjkl5 = Vjkl5()
        session.cookies["vjkl5"] = vjkl5

        list_url = "http://wenshu.court.gov.cn/List/ListContent"
        data = {
            "Param": "关键词:合同",
            "Index":index,
            "Page": 10,
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": Vl5x(vjkl5),
            "number": Number(),
            "guid": Guid(),
        }
        response = session.post(list_url, data=data, proxies=self.proxy,)
        # response = self.f.post_req(url=list_url, data=data)
        if response != False:
            json_data = json.loads(response.json())

            run_eval = json_data.pop(0)["RunEval"]
            try:
                key = parse_run_eval(run_eval)
            except ValueError as e:
                raise ValueError("返回脏数据") from e
            else:
                print("RunEval解析完成:", key, "\n")

            key = key.encode()
            # lt = []
            tag = False
            try:
                for item in json_data:
                    cipher_text = item["文书ID"]

                    plain_text = decrypt_doc_id(doc_id=cipher_text, key=key)
                    print("成功, 文书ID:", plain_text, "\n")
                    red_cli.sadd("ws_docid", str({'docid': plain_text}))
                    log.info("文书ID存入redis--{}".format(plain_text))
                    tag = True
            except:
                tag = False
                # lt.append(plain_text)
            return tag
        else:
            log.info("代理超时{}".format(self.proxy))



    def run(self):
        """
        程序主函数
        :return:
        """
        page = 1
        real_page_num = 20

        while page <= 20:


            # prox = choice(get_proxy(1))["ip"]
            proxy = self.check_ip()
            # proxy = {
            #     "http": "http://" + prox, "https": "https://" + prox,
            # }
            self.proxy = proxy

            if page > real_page_num:
                # 每个搜索条件只给20页，再多请求会给重复的或假数据
                break
            self.request_list(page)
        TAG = True
        return TAG