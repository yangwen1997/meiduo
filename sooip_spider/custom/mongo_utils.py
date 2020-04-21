import hashlib
from random import choice
from bson import ObjectId
from collections.abc import Mapping

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, DuplicateKeyError
from custom.lib_utils import md5

default_uri = 'mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017'

from pymongo.errors import AutoReconnect
from retrying import retry


def retry_if_auto_reconnect_error(exception):
    """Return True if we should retry (in this case when it's an AutoReconnect), False otherwise"""
    return isinstance(exception, AutoReconnect)


class RecordTypeError(Exception):
    def __str__(self):
        return repr('The inserted data type must be dict!!!')


class Database(object):

    def __init__(self, uri, db, maxSize=None):
        self._conn = MongoClient(uri, maxPoolSize=maxSize)
        self._db = self._conn[db]

    def create_col(self, col_name):
        """创建一个集合"""
        try:
            self._db.create_collection(col_name)
            print('collection : <%s> is creating a successful !!!'%col_name)
        except CollectionInvalid:
            print('collection : <%s> already exists !!!'%col_name)

    def drop_col(self, col_name):
        """删除一个集合"""
        status = self._db.drop_collection(col_name)
        if status['ok'] == 1.0:
            print('collection : <%s> drop successful !!!'%col_name)
        elif status['ok'] == 0.0:
            print('collection : <%s> drop failed, the collection not exist !!!'%col_name)

    def get_all_col(self):
        col_list = self._db.collection_names()
        for col in col_list:
            print('collection: <%s>'%col)
        return col_list

    @property
    def status(self):
        return self._conn is not None and self._db is not None

    def make_col(self, col):
        """连接上一个collection"""
        return Col(self._db[col], col)

    def __repr__(self):
        return '{}'.format(self._db)

class Col:

    def __init__(self, col, _col_name):
        self._local_col = col
        self._col_name = _col_name

    @property
    def count(self):
        """查看集合中的文档数量"""
        nums = self._local_col.count()
        print('current collection [%s] has <%s> record!!!'%(self._col_name, nums))
        return nums

    def find_one_and_update(self, field, before, after):
        """取出一个文档，并修改其标记位"""
        return self._local_col.find_one_and_update({field: before}, {"$set": {field: after}})

    def finished_and_update(self, _id, field, after):
        """完成写入，并移动标记位"""
        self._local_col.update({"_id": _id}, {"$set": {field: after}})

    def _check(self, data):
        """检查插入的数据类型是否是字典类型"""
        return 1 if isinstance(data, Mapping) else 0

    @retry(retry_on_exception=retry_if_auto_reconnect_error, stop_max_attempt_number=2, wait_fixed=2000)
    def insert_one(self, data, set_id_func=None, filed=None, flag=False):
        """插入单个文档"""
        if self._check(data):
            if set_id_func:
                _id = set_id_func(filed)
                data.setdefault('_id', _id)

            if flag:
                suffix = {'flag': 0, 'finished': 0}
                data.update(suffix)

            try:
                self._local_col.insert(data)
                print('download success!!! <%s>'%data['_id'])
            except DuplicateKeyError:
                print('document was exist, duplicate error !!!')
        else:
            raise RecordTypeError

    def insert_many(self, data_list):
        """批量插入"""
        ret = self._local_col.insert_many(data_list)
        return ret.inserted_ids

    def find(self, *args, **kwargs):
        """查找多个"""
        return self._local_col.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        """查找一个"""
        return self._local_col.find_one(*args, **kwargs)

    def delete_one(self, *args, **kwargs):
        """删除操作"""
        self._local_col.delete_one(*args, **kwargs)


    def delete_many(self, *args, **kwargs):
        """批量删除"""
        deletor = self._local_col.delete_many(*args, **kwargs)
        print('remove < %s > document !!!'%deletor.deleted_count)

    def flush(self):
        """清空集合"""
        self.delete_many({})

    def update_many(self, *args, **kwargs):
        """批量更新"""
        updator = self._local_col.update_many(*args, **kwargs)
        print('matched_count < %s > || modified_count < %s > !!!' %(updator.matched_count, updator.modified_count))



    def random(self):
        return choice(list(self.find()))


if __name__ == '__main__':
    db = Database('mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017', 'local_com')
    pass