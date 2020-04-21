'''
@author: 杨文龙
@file : run.py
@time: 2019/5/29
@desc:
'''

#基本模块
import re
import json


#调式
from random import choice

import execjs
import hashlib
import gc
from fake_useragent import UserAgent
from easydict import EasyDict


#本地
from wens.feach import FEACH
from wens.common import URI, DESCENDING, COLLECTION,REDIS,get_log,get_proxy
from wens.get_ip import GetIP
from wens.docid import decrypt_doc_id
from wens.docid_key import parse_run_eval
from wens.mongo import MongoDB


#全局配置
log = get_log()
#mongdo
DB = MongoDB(uri=URI,db=DESCENDING,collection=COLLECTION)
red_cli = REDIS

ua = UserAgent()

class WENS(object):
    """
    裁判文书类
    """
    def __init__(self,proxy, search):
        """
        初始化
        """
        self.f = FEACH()
        self.url = 'http://wenshu.court.gov.cn/'
        self.proxy = proxy
        self.search = search

    def base_page(self) -> str:
        """
        请求访问首页
        :return:
        """
        resp = self.f.get_req(url=self.url, proxies=self.proxy)
        if resp != False:
            dynamicurl = re.search(r'dynamicurl="(.*?)"', resp.text).group(1)
            wzwsquestion = re.search(r'wzwsquestion="(.*?)"', resp.text).group(1)
            wzwsfactor = re.search(r'wzwsfactor="(.*?)"', resp.text).group(1)
            wzwsmethod = re.search(r'wzwsmethod="(.*?)"', resp.text).group(1)
            wzwsparams = re.search(r'wzwsparams="(.*?)"', resp.text).group(1)
            para_part = '''
                   var dynamicurl="{}";var wzwsquestion="{}";var wzwsfactor="{}";var wzwsmethod="{}";var wzwsparams="{}";
                   '''.format(dynamicurl, wzwsquestion, wzwsfactor, wzwsmethod, wzwsparams)
            with open('base_js.js', 'r', encoding="utf-8") as f:
                js_code = f.read()
            js_code = para_part + js_code
            ctx = execjs.compile(js_code)
            wzwschallenge = ctx.call("wzwschallenge")
            return wzwschallenge

        else:
            return "False"

    def lt_url(self,wzwschallenge:str,page:int):
        """
        携带首页的生成url访问列表页
        :return:
        """
        base_url = "http://wenshu.court.gov.cn/WZWSRELw==?wzwschallenge=" + wzwschallenge
        resp = self.f.get_req(url=base_url,proxies=self.proxy)
        if resp != False:
            lt_url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++{}'.format(self.search)
            # lt_url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
            if resp != False:
                res = self.f.get_req(url=lt_url,proxies=self.proxy)
                if res != False:
                    vjkl5 = self.f.session.cookies.get('vjkl5')

                    #生成guid
                    with open('guid.js', 'r', encoding="utf-8") as f:
                        js_code = f.read()
                    ctx = execjs.compile(js_code)
                    guid = ctx.call("ref")

                    #生成vl5x
                    with open('vl5x.js', 'r', encoding="utf-8") as f:
                        js_code = f.read()
                    ctx = execjs.compile(js_code)
                    vl5x = ctx.call("getCookie", vjkl5)

                    self.f.session.headers.update(
                        {"X-Requested-With": "XMLHttpRequest"}
                    )
                    data = {
                        "Param": "{}".format(self.search),
                        "Index": page,
                        "Page": 10,
                        "Order": "法院层级",
                        "Direction": "asc",
                        "vl5x": vl5x,
                        "number": 'wens',
                        "guid": guid,

                    }
                    list_url = 'http://wenshu.court.gov.cn/List/ListContent'
                    resp = self.f.post_req(url=list_url,data=data,proxies=self.proxy)
                    if resp != False:
                        docid_text = json.loads(resp.json())
                        return docid_text
                    else:
                        return "False"
                else:
                    return "False"
            else:
                return "False"
        else:
            return "False"

    def RunEval_parse(self,docid_LT)->list:
        """
        解密docid
        :param docid_LT:
        :return:
        """

        run_eval = docid_LT.pop(0)["RunEval"]
        key = parse_run_eval(run_eval)

        key = key.encode()

        lt = list()
        global tags
        try:
            for item in docid_LT:

                cipher_text = item["文书ID"]
                # print("解密:", cipher_text)
                plain_text = decrypt_doc_id(doc_id=cipher_text, key=key)
                print("成功, 文书ID:", plain_text, "\n")
                # lt.append(plain_text)
                red_cli.sadd("ws_docid", str({'docid':plain_text}))
                log.info("文书ID存入redis--{}".format(plain_text))
                tags = True
        except:
            tags = False
        return tags

    def save_data(self,docid_list:list):
        """
        解析页面保存数据
        :return:
        """

        tag = 1
        try:
            for _ in docid_list:
                url_ = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(_)

                result = self.f.get_req(url=url_, proxies=self.proxy)
                if result != False:
                    item = EasyDict()

                    json_dict = re.search(r'var caseinfo=JSON.stringify\((?P<case_info>.+?)\);\$'
                                          r'.+var jsonHtmlData = (?P<html_data>".+");',result.text, re.S).groupdict()
                    item._id = hashlib.md5(str(url_).encode('utf-8')).hexdigest()
                    item.info = json_dict
                    DB.mongo_add(item)
                    tag = 2
        except:
            tag = 3
        return tag

    def check_ip(self):
        """
        获取IP
        :return:
        """
        # IP = GetIP()
        while 1:
            # pro = IP.get_jt()
            # prox = eval(pro)["ip"]

            prox = choice(get_proxy(1))["ip"]
            proxy = {
                "http": "http://" + prox, "https": "https://" + prox,
            }
            check_pro = {"ip": proxy["http"]}
            tag = red_cli.sismember("wenshu_bad_ip", str(check_pro))

            if tag:
                print("该IP存在失效IP池中，不能使用")
            else:
                return proxy

    def run(self):
        """
        程序主函数
        :return:
        """
        page = 1
        real_page_num = 20

        while page <= 20:

            if page > real_page_num:
                # 每个搜索条件只给20页，再多请求会给重复的或假数据
                break

            wzwschallenge = self.base_page()
            if wzwschallenge != "False":
                docid_LT = self.lt_url(wzwschallenge, page)

                if docid_LT != "False":
                    try:
                        global docid_list
                        docid_list = self.RunEval_parse(docid_LT)

                        if docid_list:
                            log.info("该页数据保存完毕")
                            page += 1
                            gc.collect()
                        else:
                            pass


                    except:
                        log.info("解析异常")
                else:
                    self.proxy = self.check_ip()
            else:
                self.proxy = self.check_ip()
        
        TAG = True
        return TAG