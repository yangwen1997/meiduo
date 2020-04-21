#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 静态代理拨号
import pymongo, time
client_55 = pymongo.MongoClient('mongodb://root:root962540@10.0.0.55:27017')
ip_results_coll = client_55['ip_db']['vps_static_ip_results']

while True:
    now_time = int(time.strftime("%H", time.localtime()))
    res = ip_results_coll.find()
    if now_time in [12, 0]:
        for _ in res:
            ip_results_coll.update_one({'_id':_.get('_id')}, {'$set':{'flag': False}})
            print('sleep 60s...')
            time.sleep(120)
        print('全部拨号完成')
        time.sleep(3600)
    else:
        time.sleep(120)