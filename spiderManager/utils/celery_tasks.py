# -*- coding: utf-8 -*-
import datetime
import sys
sys.path.append('..')
sys.path.append('../../')
from celery import task
import pymongo
import requests
import os, time
import django
from celery import Celery
from django.db.models import Sum
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from spiderManager.utils.celery_tasks import *



# # set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiderManager.settings')
# Setup django project
django.setup()

# Setup celery
app = Celery('celery_workers')
app.config_from_object('django.conf:settings')

import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
from utils.news_list import list_run
from utils.news_details import details_run
from counter.models import Counter,Types,SumNum





@task
def sum_counter(): # 统计增量
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    all = Counter.objects.filter(timestamp=yesterday)
    instances = Types.objects.all()
    for t_name in instances:
        _id = t_name.id
        sum_all = all.filter(typec_id=_id).aggregate(Sum('record'))
        SumNum.objects.create(typec_id=_id, number=sum_all['record__sum'])
    return 'success'

@task
def check_counter(db,collection, name,type,uri=None):
    # 从mongodb数据库中把数据取出然后通过请求的方式存入sqlite3中
    if uri == None:
        client = pymongo.MongoClient(
        'mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017')
    else:
        client = pymongo.MongoClient(uri)
    col = client[db][collection]
    num = col.find().count()
    rep = requests.post('http://10.0.0.55:9998/counter/data_handler',
                        data={'name': name, 'number': num, 'collection': collection,'type':type})

    return rep


@task(ignore_result=True, expires=3600) # 新闻
def chrome():
    list_run()
    details_run()


@task(ignore_result=True, expires=3600) #
def clear_ips(col="bad_ips"):
    db = pymongo.MongoClient("mongodb://root:root962540@10.0.0.55:27017")
    c = db['ip_db']
    c.drop_collection(col)


@task(ignore_result=True, expires=3600)
def change_ip_status(db ='ip_db' ,col="ip_lists"):
    client = pymongo.MongoClient("mongodb://root:root962540@10.0.0.55:27017")
    col = client[db][col]
    col.update_many({}, {'$set': {'flag': False}})


check_counter.delay('redis://:dgg962540@127.0.0.1:6379/1','all_com', '3_all_results','名录',uri=None)

def innit_type_in_db():
    basic = ['微猫','企查查','工信中国','企查查基本信息','水滴信用详情','百度信用基本信息','启信宝基本信息','企查猫基本信息']
    names = ['名录','启信名录','企查查名录']
    logos = ['智高点商标','千慧网商标']
    lows = ['无讼文书','裁判文书']
    zz = ['建筑资质']
    other = ['企查查资产']
    # Types.objects.create(name='名录')
    # Types.objects.create(name='商标')
    # Types.objects.create(name='法律')
    # Types.objects.create(name='资质')
    Types.objects.create(name='其他')
    for i in basic:
        Counter.objects.filter(name=i).update(typec_id = 1)
    for i in names:
        Counter.objects.filter(name=i).update(typec_id=2)
    for i in logos:
        Counter.objects.filter(name=i).update(typec_id=3)
    for i in lows:
        Counter.objects.filter(name=i).update(typec_id=4)
    for i in zz:
        Counter.objects.filter(name=i).update(typec_id=5)
    for i in other:
        Counter.objects.filter(name=i).update(typec_id=6)


if __name__ == '__main__':
    input('是否创建相对应的外键关系?')
    innit_type_in_db()
