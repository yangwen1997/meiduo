import time
import json
from common import redis_conn, account_results_coll


def list_from_db():
    key = 'tyc_account_lists'
    while True:
        key_num = redis_conn.lenList(key)
        if key_num < 100:
            timeout = str(int(time.time() * 1000) - 86400000)
            res = account_results_coll.find(
                {
                    "flag": 10,
                    '$or': [{'updateTime': {'$exists': False}}, {'updateTime': {'$lt': timeout}}],
                    'usable': 0,
                }
            ).limit(500)
            if res.count() != 0:
                for _ in res:
                    # print(_.get('_id'))
                    # del _['_id']
                    redis_conn.pushLink(key, json.dumps(_))
                print('[INFO]: 补充数据完成')
            else:
                print('[INFO]: 没有符合条件的数据')
                break
        print('[INFO]: sleep 30s\n')
        time.sleep(30)

def check_cookie():
    key = 'check_cookie'
    res = account_results_coll.find({'flag': {'$in': [1, 11, 2]}, 'usable': 0})
    for _ in res:
        redis_conn.pushLink(key, json.dumps(_))
    print('[INFO]: 补充数据完成')


if __name__ == '__main__':
    # check_cookie()
    list_from_db()