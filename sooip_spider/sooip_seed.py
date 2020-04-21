import re
import datetime
from random import choice
import redis
import requests
from custom.proxy_utils import IpPool
from redis_config import *

# post请求参数配置
PAT_TYPE = "pdb = 'USA0' OR pdb = 'USB0' OR pdb = 'USS0'"  #美国的专利参数


'''
负责生成日期，根据每个日期抓取专利列表接口，获取该日期当天专利公开的总数目,并计算出分页参数存入redis队列。
'''


class CookiesPool(object):
    """
    从cookies池随机获取一个cookie
    """
    def __init__(self):
        self.conn = redis.Redis(host=HOST, db=DB,password=PASSWORD)
        self.key = 'cookies:sooip:*'

    def random(self):
        """
        从redis队列随机获取一个cookie
        :return: dict
        """
        keys = self.conn.keys(self.key)
        raw_cookie = self.conn.get(choice(keys))
        cookie = eval(raw_cookie.decode("utf8"))
        return cookie


class SooipSpider(object):
    def __init__(self):
        self.conn = redis.Redis(host=HOST, db=DB,password=PASSWORD)
        self.key = 'sooip_seed'
        self.list_url = "http://www.sooip.com.cn/txnPatentData01.ajax"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Referer': 'http://www.sooip.com.cn/app/patentlist',
        }
        self.proxy_client = IpPool(20)
        self.cookie_pool = CookiesPool()

    def save(self, data):
        """
        往队列里存入一条数据
        :param data:
        :return:
        """
        self.conn.lpush(self.key, data)
        print('成功插入一条数据：%s'%data)

    def main(self, start, end):
        """
        主程序入口
        :param start:查询的开始日期
        :param end: 查询结束的日期
        :return:
        """
        #生成时间，然后以时间为参数去做查询
        # 开始时间
        datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        # 结束时间
        dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        # 遍历每一天
        while datestart <= dateend:
            # 当前查询日期
            date = datestart.strftime('%Y%m%d')
            print('current date is 【%s】'%date)
            # 日期加一天
            datestart += datetime.timedelta(days=1)
            # 构建请求参数
            data = self.param(date)
            # 下载数据
            html = self.download(data)
            self.parse(html, date)

    def param(self, date):
        """
        构建请求参数
        :param date: 公告日期
        :return:
        """
        #构建param
        data = {
            "secondKeyWord": "名称+摘要+主权项",
            "secondkeyWordVal": "",
            "secondSearchType": "AND",
            "attribute-node:patent_cache-flag": "false",
            "attribute-node:patent_start-row": '1',
            "attribute-node:patent_page-row": "50",
            "attribute-node:patent_sort-column": "ano",
            "attribute-node:patent_page": "1",
            "express2": "",
            "express": "(公开（公告）日 =  ( %s ) )" % date,
            "isFamily": "",
            "categoryIndex": "",
            "selectedCategory": "",
            "patentLib": PAT_TYPE,
            "patentType": "patent2",
            "order": "",
            "pdbt": "",
        }
        return data

    def count_total(self, html):
        #计算返回某一天根据公开日期查询到的专利总数
        total = re.search(r'<patent_record-number>(\d+)</patent_record-number>', html, re.S).group(1)
        return int(total)

    def download(self, data):
        #下载重试5次，
        count = 5
        while count > 0:
            try:
                # 获取代理
                proxies = {'http': self.proxy_client.get(type='http')}
                resp = requests.post(self.list_url, headers=self.headers, data=data, proxies=proxies, cookies=self.cookie_pool.random(), timeout=5)
                if resp.status_code == 200:
                    # 检查IP或者cookie是否失效
                    if check(resp.text):
                        return resp.text
                    else:
                        raise Exception('Invalid')
            except Exception:
                self.proxy_client.switch()
                count -= 1
        return None

    @staticmethod
    def compute(total):
        #计算 接口每次最大能获取50条能获取1000页。跟着这个来计算start参数
        res = []
        if total != 0:
            # 取模获取页数
            page, v = divmod(total, 50)
            # 有余数，则页数+1
            if v != 0:
                page += 1
            # 最大能翻1000，所以大于1000页的不做处理
            if page > 1000:
                page = 1000
            start = 1
            # 计算翻页页码的请求参数
            for i in range(1, page + 1):
                res.append(start)
                start = i * 50 + 1
        return res

    def parse(self, html, date):
        """
        页面解析
        :param html: 页面HTML
        :param date: 日期
        :return:
        """
        # 统计当前公告日期的专利总数
        total = self.count_total(html)
        for start in SooipSpider.compute(total):
            item = {'start': start, 'date': date}
            self.save(item)

    def test(self):
        #测试用
        date = '20150210'
        data = self.param(date)
        html = self.download(data)
        self.parse(html, date)


def check(text):
    #查看是否ip或cookie失效
    if not re.search('访问无效！', text):
        return True
    return False


if __name__ == '__main__':
    obj = SooipSpider()
    obj.main('2014-01-08', '2019-01-23')

