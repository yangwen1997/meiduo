#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019/1/4 9:50
@Author  : 方甜
@File    : names_to_redis.py
@Software: PyCharm
@Version : 1.0
@Desc    : 读取姓名到redis队列作为天眼查查询名录的条件
"""
import time
import json
from common import redis_conn, name_results_coll, pymongo, local_all_com



def list_from_db():
    key = 'tyc_name_lists'
    txt = 'last_index.txt'
    while True:
        key_num = redis_conn.lenList(key)
        if key_num > 10000:
            print('[INFO]: sleep 10s\n')
            time.sleep(10)
            continue
        else:
            with open(txt, 'r') as f:
                index = f.read()
            res = name_results_coll.find(
                {"name_num": {'$exists': False}, '_id': {'$gt': index}}
            ).sort('_id', pymongo.ASCENDING).limit(100)
            count = 0
            for _ in res:
                redis_conn.pushLink(key, json.dumps(_))
                with open(txt, 'w') as f:
                    f.write(_.get('_id'))
                count += 1
            if count:
                print('[INFO]: 补充数据完成')
            else:
                print('[INFO]: 没有符合条件的数据')
                continue



def list_from_db_chengdu():
    key = 'tyc_name_chengdu_lists'
    while True:
        key_num = redis_conn.lenList(key)
        if key_num < 500:
            res = local_all_com['rongzi_chendu'].find(
                {'companyTel': {'$in': [None, '']}, 'flag': 0}
            )
            if res.count() != 0:
                for _ in res:
                    # print(_.get('_id'))
                    # del _['_id']
                    redis_conn.pushLink(key, json.dumps(_))
                print('[INFO]: 补充数据完成')
            else:
                print('[INFO]: 没有符合条件的数据')
                quit()
        print('[INFO]: sleep 10s\n')
        time.sleep(10)

def second_list_from_db():
    '''
    第二种方案读取搜索列表方式
    查询条件有四种：
        # 这种是之前数量搜索结果数量太大（100000+）或者有段时间企查查改版搜索结果大于5000都显
        示的是5000+的情况(count:5500)
        1. query = {'company_numm':0, name_num:{'$ne':0}}

        # 这种是之前搜索不出来结果的（有可能是搜索范围过大，或者是IP访问过频繁本来有结果的，
        网站返回搜索不到结果的）需要重新请求(count=367124)
        2. query = {'company_numm':0, name_num:0}

        # 这种是之前抓取搜索结果在100条以内，但是可能是因为网站改版或者网络问题没有入库成功的数
        据，需要重新请求(count=2552094)
        3. query = {'company_numm':{'$lte':100,'$gt':0},'flag':{'$eq': 0}}dgg962540

        # 这种是之前没有抓过的搜索结果大于100条的(count=3956299)
        4. query = {'company_numm':{'$gt': 100}, 'flag': {'$ne': 1}}
        备注: flag==1已经抓取过的

    redis_conn       : redis连接对象
    name_results_col : mongodb表连接对象（database: tyc_com.name_results）
    '''
    # redis的key
    key = 'tyc_name_lists'
    # 查询条件
    query = {'company_numm': {'$lte': 100, '$gt': 0}, 'flag': {'$eq': 0}}
    while True:
        # 查询当前队列中名字的数量
        key_num = redis_conn.lenList(key)
        # 如果数量大于1万则不补充，否则从数据库中读取符合条件的数据补充都队列中
        if key_num > 1000:
            print('[INFO]: sleep 10s\n')
            time.sleep(10)
            continue
        else:
            res = name_results_coll.find(query).limit(20000)
            count = 0
            for _ in res:
                redis_conn.pushLink(key, json.dumps(_))
                count += 1
            # 如果count不等于0表示有数据补充完成，否则表示没有符合条件的数据
            if count:
                print('[INFO]: 补充数据完成')
            else:
                print('[INFO]: 没有符合条件的数据')
                time.sleep(180)
                continue


if __name__ == '__main__':
    # list_from_db()
    # list_from_db_chengdu()
    second_list_from_db()