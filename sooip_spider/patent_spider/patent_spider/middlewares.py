import re
from random import choice
import redis
from patent_spider.utils.common import ProxyPool
# redis配置
DB = 4
HOST = '10.2.1.91'
PASSWORD = 'Dgg!@76322658'
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
        self.conn = redis.Redis(host=HOST, db=DB,password=PASSWORD)
        self.key = 'cookies:sooip:*'

    def random(self):
        keys = self.conn.keys(self.key)
        raw_cookie = self.conn.get(choice(keys))
        cookie = eval(raw_cookie.decode("utf8"))
        return cookie

    def process_request(self, request, spider):
        #目前只有这3个接口需要cookie
        if request.url.startswith('http://www.sooip.com.cn/app/patentdetail'): #专利公开信息接口
            request.cookies = self.random()
        if request.url.startswith('http://www.sooip.com.cn/app/authorization'): #专利授权信息接口
            request.cookies = self.random()
        if request.url.startswith('http://www.sooip.com.cn/app/lawdetail?pid='):  #法律状态信息接口
            request.cookies = self.random()
        return None


class SwitchMiddleware(object):
    #专利信息分为两种模式一种是专利公开信息，一种是专利授权信息。部分专利只有专利授权或者专利公开。
    #在外面发起的请求都是先获取专利公开信息的。如果返回页面没有专利公开信息，那就在这里替换为专利授权并重发。
    def process_response(self, request, response, spider):
        if re.search('当前专利没有公开详情', response.text, re.S):
            print('switch_url')
            request = request.replace(url=request.url.replace('patentdetail', 'authorization'))
            return request
        return response


