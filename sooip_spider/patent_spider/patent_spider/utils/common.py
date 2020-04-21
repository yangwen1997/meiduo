from random import choice
import redis
import pymongo
from patent_spider.settings import *

# redis配置
DB = 4
HOST = '10.2.1.91'
PASSWORD = 'Dgg!@76322658'

class ProxyPool:
    #切换代理。count字段是每个代理用10次就切换。
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


class RedisClient:
    def __init__(self):
        self.conn = redis.Redis(host=HOST,password=PASSWORD, db=1)
        self.key = "sooip_com"

    def pop(self):
        return eval(self.conn.lpop("sooip_com").decode("utf8"))

    def fetch_one(self):
        return self.pop()

    def fetch_many(self, count):
        return [self.pop() for _ in range(count)]


class MyMongo:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.col = self.db['sooip_list_us']

    def finished(self, ID):
        self.col.update({'_id': ID}, {'$set': {'finished': 1}})


