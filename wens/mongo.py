from pymongo import MongoClient
import time
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError


class MongoDB(object):
    """
    输入一个数据库链接地址、数据库名称（字符串）、collection名称（字符串），不存在则创建
    """

    def __init__(self, uri, db, collection, pool_size=100):
        self._client = MongoClient(uri, maxPoolSize=pool_size)
        self.db = db
        self.collection = collection
        self.wait = time.sleep(2)

    # get /creat a mongo database
    def get_database(self):
        if self._client:
            return self._client.get_database(self.db)
        else:
            raise Exception("MongoClient connection failed")

    # get /creat a mongo collection
    def get_collection(self):
        return self.get_database().get_collection(self.collection)

    def mongo_add(self, dic):
        try:
            self.get_collection().insert_one(dic)
            print('%s 插入成功 !!!!' % dic['_id'])
        except DuplicateKeyError:
            print('数据重复，已经忽略')
        except ServerSelectionTimeoutError:
            print('MongoDB连接出错，等待重试中……')
            self.wait()
            return self.get_collection().insert_one(dic)

    def mongo_addmany(self, dics):
        self.get_collection().insert_many(dics)

    def mongo_find(self, dic):
        return self.get_collection().find(dic)

    def mongo_update(self, filters, updater):
        self.get_collection().update(filters, {"$set": updater})

    # delete a database
    def mongo_deldb(self):
        self._client.drop_database(self.db)

    # delete a collection
    def mongo_delcol(self):
        self.get_database().drop_collection(self.collection)

    # delete all documents
    def mongo_delall(self):
        self.get_collection().remove()

    # delete a document
    def mongo_delone(self, dic):
        self.get_collection().remove(dic)

    def close(self):
        self._client.close()


if __name__ == '__main__':
    def test():
        db = MongoDB('127.0.0.1:27017', 'test', 'test_coll')

        # 增加1条数据
        db.mongo_add({'name': 1})

        # 增加2条数据
        db.mongo_addmany([{'age': 2, 'score': 3}, {'score': 3}])
