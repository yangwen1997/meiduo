import re
from random import choice

import redis
import pymongo

from patent_spider.settings import *


class ProxyPool:
    def __init__(self):
        self.client = pymongo.MongoClient(IP_URI)[IP_DB][IP_COL]
        self.random()
        self.count = 0

    def random(self):
        item_list = list(self.client.find())
        proxy = 'http://' + choice(item_list)['ip']
        self.proxy = proxy

    def pop(self):
        self.count += 1
        if self.count >= 10:
            self.random()
            self.count = 0
        return self.proxy


def count_total(html):
    total = re.search(r'<patent_record-number>(\d+)</patent_record-number>', html, re.S).group(1)
    return int(total)


def compute(total):
    res = []
    if total != 0:
        page, v = divmod(total, 50)
        if v != 0:
            page += 1
        if page > 1000:
            page = 1000
        start = 1
        for i in range(1, page + 1):
            res.append(start)
            start = i * 50 + 1
    return res


def extract_by_re(node, exp):
    """提取"""
    pattern = re.compile(exp, re.S)
    try:
        res = pattern.search(node).group(1)
        return res
    except AttributeError:
        return None


deal_drap = lambda s: s.split('|')[1:] if s is not None else None


class RFPDupeFilter:
    def __init__(self):
        self.server = redis.Redis(host='10.2.1.91', port=6379, db=5)
        self.key = 'sooip_dupefilter'

    def request_seen(self, request):
        fp = request
        added = self.server.sadd(self.key, fp)
        return added == 0






