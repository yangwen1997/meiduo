import hashlib
import re
from functools import partial
from random import choice
import redis
import requests
from custom.mongo_utils import Database, default_uri
from custom.proxy_utils import IpPool
from redis_config import *


#配置
MONGO_DB = 'patent_com'
MONGO_COL = 'sooip_list_us'

PAT_TYPE = "pdb = 'USA0' OR pdb = 'USB0' OR pdb = 'USS0'"  #美国的专利参数，中国的把这个改了就行。
#redis密码

class CookiesPool(object):
    def __init__(self):
        self.conn = redis.Redis(host=HOST, db=DB,password=PASSWORD)
        self.key = 'cookies:sooip:*'

    def random(self):
        keys = self.conn.keys(self.key)
        raw_cookie = self.conn.get(choice(keys))
        cookie = eval(raw_cookie.decode("utf8"))
        return cookie


def extract_by_re(node, exp):
    """封装下re"""
    pattern = re.compile(exp, re.S)
    try:
        res = pattern.search(node).group(1)
        return res
    except AttributeError:
        return None


deal_drap = lambda s: s.split('|')[1:] if s else None


class SooipSpider(object):
    def __init__(self):
        self.conn = redis.Redis(host=HOST, db=DB,password=PASSWORD)
        self.key = 'sooip_seed'
        self.list_url = "http://www.sooip.com.cn/txnPatentData01.ajax"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Referer': 'http://www.sooip.com.cn/app/patentlist',
        }
        self.mongo_client = Database(default_uri, MONGO_DB).make_col(MONGO_COL)
        self.proxy_client = IpPool(20)
        self.cookie_pool = CookiesPool()

    def pop(self):
        return eval(self.conn.rpop(self.key).decode('utf8'))

    def param(self, item):
        data = {
            "secondKeyWord": "名称+摘要+主权项",
            "secondkeyWordVal": "",
            "secondSearchType": "AND",
            "attribute-node:patent_cache-flag": "false",
            "attribute-node:patent_start-row": item['start'],
            "attribute-node:patent_page-row": "50",
            "attribute-node:patent_sort-column": "ano",
            "attribute-node:patent_page": "1",
            "express2": "",
            "express": "(公开（公告）日 =  ( %s ) )" % item['date'],
            "isFamily": "",
            "categoryIndex": "",
            "selectedCategory": "",
            "patentLib": PAT_TYPE,
            "patentType": "patent2",
            "order": "",
            "pdbt": "",
        }
        return data

    def download(self, data):
        count = 5
        while count > 0:
            try:
                proxies = {'http': self.proxy_client.get(type='http')}
                resp = requests.post(self.list_url, headers=self.headers, data=data, proxies=proxies, cookies=self.cookie_pool.random(), timeout=15)
                if resp.status_code == 200:
                    return resp.text
            except Exception:
                self.proxy_client.switch()
                count -= 1
        return None

    def parse(self, html):
        """
        列表页解析
        :param html:
        :return:
        """
        nodes = re.findall(r'<patent>(.*?)</patent>', html, re.S)
        for node in nodes:
            extract = partial(extract_by_re, node)
            pid = extract('<PID>(\w*?)</PID>')
            ano = extract('<ANO>(.*?)</ANO>')
            if '.' in ano:
                ano = ano.split('.')[0]
            abs = extract('<ABSO>(.*?)</ABSO>') or extract('<DEBEO>(.*?)</DEBEO>') #专利类型如果外观专利，则只有DEBEO是描述信息，否则只有ABSO为摘要。
                                                                                   #这里or操作符 如果ABSO存在则返回前面的 否则直接返回后面的。
            raw_drap = extract('<DRAP>(.*?)</DRAP>')
            drap = deal_drap(raw_drap)
            item = {'_id': hashlib.md5(ano.encode('utf8')).hexdigest(),
                    'applyCode': ano,
                    'absInfo': abs,
                    'desDrawings': drap,
                    'pid': pid}
            self.mongo_client.insert_one(item, flag=True)

    def main(self):
        while 1:
            item = self.pop()
            data = self.param(item)
            html = self.download(data)
            self.parse(html)


if __name__ == '__main__':
    spider = SooipSpider()
    spider.main()


