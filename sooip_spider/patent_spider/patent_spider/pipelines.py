import logging
import pymongo
from pymongo.errors import DuplicateKeyError
from patent_spider.utils.common import MyMongo
client = MyMongo()


class PatPipeline(object):
    #主要处理数据入库，图片存储格式更改。

    def __init__(self, mongo_uri, mongo_db, mongo_col, stats):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_col=crawler.settings.get('MONGO_COL'),
            stats=crawler.stats  #数据收集器，用于记录成功抓取总数的
        )

    def open_spider(self, spider):
        '''连接数据库'''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.col = self.db[self.mongo_col]

    def process_item(self, item, spider):
        '''数据操作：存入数据库'''
        try:
            new_item = self.gen_data(item)
            client.finished(new_item['_id'])
            self.col.insert(new_item)
            print('%s download success !!!!!' % item['_id'])
        except DuplicateKeyError:
            logging.error('DuplicateKeyError by %s' % item['_id'])
        self.stats.inc_value('item_count')
        return item

    def gen_data(self, item):
        imgNameList = ['desDrawings', 'claImg', 'desImg']
        for imgName in imgNameList:
            res = []
            opt = item['docs']['imgUrls'][imgName]
            if opt is None:
                item['docs']['imgUrls'][imgName] = []
                continue
            if len(opt) != 0:
                for i, url in enumerate(opt):
                    clName = self.__gen_name(item['_id'], imgName, i, url)
                    line = {'clName': clName, 'clUrl': url, 'clPath': None}
                    res.append(line)
            item['docs']['imgUrls'][imgName] = res
        return item

    @staticmethod
    def __gen_name(ID, imgName, index, url):
        name = ID + '@' + 'docs#imgUrls#' + imgName + '[' + str(index) + ']' + '@' + url.replace(':', '~').\
            replace('/', '！').replace('?', ';')
        return name

    def close_spider(self, spider):
        '''关闭数据库'''
        print('finished item: [%s]'%self.stats.get_value('item_count'))
        self.client.close()