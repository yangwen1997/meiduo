import os
import time
from random import choice

from gevent import monkey; monkey.patch_all()
import gevent
import requests

import pymongo

MONGO_URI = "mongodb://root:root962540@10.0.0.55:27017"
MONGO_DB = "ip_db"
MONGO_COL = "ip_results"


class ProxyPool:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)[MONGO_DB][MONGO_COL]
        self.random()
        self.count = 0

    def random(self):
        item_list = list(self.client.find())
        proxy = 'http://' + choice(item_list)['ip']
        self.proxy = proxy

    def mark(self):
        self.count += 1
        if self.count >= 40:
            self.random()
            self.count = 0

    def pop(self):
        return self.proxy

class Tomongo:
    def __init__(self):
        self.client = pymongo.MongoClient(
            'mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017')
        self.db = self.client["patent_com"]

        self.detail_results = self.db['detail_results']
        self.record = self.db['record']

    def fetch(self):
        item = self.detail_results.find_one_and_update({'flag': 0}, {"$set": {"flag": 1}})
        # item=self.detail_results.find_one({'flag': 0})
        return item

    def record_fail(self, item):
        self.record.insert(item)
        print('下载失败%s'%item)

    def finished(self, ID):
        self.detail_results.update({'_id': ID}, {"$set": {'flag': 2}})
        print('id为：【%s】的图片下载完毕'%ID)


def retry(num_retries=1, interval=0.5):
    print('重试中~~~')
    def wrapper(func):
        def wrapper(*args,**kwargs):
            last_exception =None
            for _ in range(num_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                finally:
                    time.sleep(interval)
            # raise last_exception
            return None
        return wrapper
    return wrapper


class PatImage(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': '123.138.111.182:8804',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        }
        self.client = Tomongo()
        self.proxy = ProxyPool()

    @staticmethod
    def process_item(item):
        ID = item['_id']
        imgUrls = []
        keys = ['desDrawings', 'claImg', 'desImg']
        for key in keys:
        	try:
	            if len(item['docs']['imgUrls'][key]) != 0:
	                for v in item['docs']['imgUrls'][key]:
	                    imgName, imgUrl = v['clName'], v['clUrl']
	                    i = {'name': imgName, 'url': imgUrl}
	                    imgUrls.append(i)
	        except Exception:
	        	pass
        return ID, imgUrls

    def get_item(self):
        item = self.client.fetch()
        ID, imgItems = self.process_item(item)
        if len(imgItems) == 0:
            self.client.finished(ID)
        else:
            return ID, imgItems

    @retry(num_retries=3)
    def single_download(self, ID, imgItem):
        # proxy = self.proxy.pop()
        fileName = imgItem['name']
        resp = requests.get(imgItem['url'], headers=self.headers, stream=True)
        if resp.status_code == 200:
            print('download %s'%imgItem['url'])
            self.save_file(resp, fileName)
        else:
            record = {'detail_id': ID, 'imgName': fileName, 'imgUrl': imgItem['url'], 'flag': 0}
            self.client.record_fail(record)

    def save_file(self, resp, fileName):
        with open(fileName, "wb") as f:
            for chunk in resp.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)

    def main(self):
        while True:
            data_tuple = self.get_item()
            if data_tuple:
                ID, imgItems = data_tuple
                for imgItem in imgItems:
                    self.single_download(ID, imgItem)
                self.client.finished(ID)


def __init_catalogue():
    path = r"G:\图片1"
    os.chdir(path)


def run():
    crawler = PatImage()
    crawler.main()


def main():
    gevent.joinall([gevent.spawn(run) for _ in range(4)])


if __name__ == '__main__':
    __init_catalogue()
    main()
