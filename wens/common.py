"""
@author : yangwenlong
@file   : 公共文件
@time   ：2019/5/20 14:37
@desc
"""
import os
import logging
from pymongo import MongoClient, DESCENDING
import time
from random import choice
from pymongo.errors import ServerSelectionTimeoutError
import redis


#代理ip地址
ip_cli = MongoClient("mongodb://root:root962540@10.0.0.55:27017")
ip_results_coll = ip_cli['ip_db']['ip_results']
# ip_results_coll = ip_cli['ip_db']['vps_static_ip_results']

#本地redis
REDIS = redis.Redis(host='127.0.0.1',port=6379)


#mongodb地址
# URI = 'mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017'
URI = 'mongodb://127.0.0.1:27017'
DATABASE = 'wenshu_cn'
COLLECTION = 'y_ws_dict_info'


def get_proxy(tag=1):
    """
    获取代理
    :param
    :return:
    """

    ip_list = []
    if tag == 1:
        ip_info = ip_results_coll.find()
        for _ in ip_info:
            ip_list.append({'ip':_.get('ip'), 'mac':_.get('mac')})
    else:
        new_ip = [
            '43.240.14.47:22404',
            '43.240.14.5:22404',
            '43.240.14.158:22404',
            '43.240.14.162:22404',
            '103.39.110.172:22404',
            '43.240.14.220:22404',
            '43.240.14.223:22404',
            '43.240.14.171:22404',
            '43.240.13.183:22404',
            '43.240.14.153:22404',
        ]
        ip_list.extend(new_ip)
    return [_ for _ in ip_list]

#log日志
def logger(FILE_NAME):
    """
    日志配置
    :param FILE_NAME: 日志文件名(全路径 )
    :return:object
    """

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y %H:%M:%S',
        filename=FILE_NAME,
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging

def get_log():
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + "/log/"
    file_name = "{}_shangbiao_{}.log".format(real_path,
                                             time.strftime("%Y-%m-%d",
                                                           time.localtime()))

    log = logger(file_name)
    return log