import pymongo
import redis
from pymongo.errors import AutoReconnect
from retrying import retry
from redis_config import *


def retry_if_auto_reconnect_error(exception):
    """Return True if we should retry (in this case when it's an AutoReconnect), False otherwise"""
    return isinstance(exception, AutoReconnect)


class MyMongo:
    def __init__(self):
        self.client = pymongo.MongoClient(
            'mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017')

        self.db = self.client["patent_com"]
        self.col = self.db['sooip_list_us']

    @retry(retry_on_exception=retry_if_auto_reconnect_error, stop_max_attempt_number=2, wait_fixed=2000) #出现定义类型的错误重试
    def set_flag(self, ID):
        self.col.update({'_id': ID}, {'$set': {'flag': 1}})


class MyRedis:
    def __init__(self):
        self.local_conn = redis.Redis(host=HOST,password=PASSWORD, db=1)
        self.key = "sooip_com"
        self.mongo_client = MyMongo()

    def main(self):
        while True:
            if self.local_conn.llen(self.key) >= 300000:
                break

            item_list = self.mongo_client.col.find({'flag': 0}).limit(10000)
            for item in item_list:
                self.mongo_client.set_flag(item['_id'])
                self.local_conn.lpush(self.key, str(item))
                print(item['_id'])



if __name__ == '__main__':
    m = MyRedis()
    m.main()
