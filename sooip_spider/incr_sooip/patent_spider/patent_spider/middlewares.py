import re
from random import choice


import redis

from patent_spider.utils.common import ProxyPool

client = ProxyPool()


class UserAgentMiddlware(object):
    """设置请求头"""
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')


class ProxyMiddleware(object):
    """代理中间件"""

    def process_request(self, request, spider):
        proxy = client.pop()
        request.meta['proxy'] = proxy
        return None

    def process_response(self, request, response, spider):
        pattern = re.compile("<h1>访问无效！</h1>")
        if pattern.search(response.text):
            client.random()
            return request
        return response

    def process_exception(self, request, exception, spider):
        client.random()
        return request


class CookiesMiddleware(object):
    def __init__(self):
        self.conn = redis.Redis(host='10.2.1.91', port=6379, db=4)
        self.key = 'cookies:sooip:*'

    def random(self):
        keys = self.conn.keys(self.key)
        raw_cookie = self.conn.get(choice(keys))
        cookie = eval(raw_cookie.decode("utf8"))
        return cookie

    def process_request(self, request, spider):
        if request.url.startswith('http://www.sooip.com.cn/app/patentdetail'):
            request.cookies = self.random()
        if request.url.startswith('http://www.sooip.com.cn/app/authorization'):
            request.cookies = self.random()
        if request.url.startswith('http://www.sooip.com.cn/app/lawdetail?pid='):
            request.cookies = self.random()
        if request.url.startswith('http://www.sooip.com.cn/txnPatentData01.ajax'):
            request.cookies = self.random()
        return None


class SwitchMiddleware(object):
    def process_response(self, request, response, spider):
        if re.search('当前专利没有公开详情', response.text, re.S):
            print('switch_url')
            request = request.replace(url=request.url.replace('patentdetail', 'authorization'))
            return request
        return response


