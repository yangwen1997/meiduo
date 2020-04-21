import pymongo, json, requests, logging, hashlib, time
from pymongo import ReadPreference
from pymongo.errors import DuplicateKeyError
from redisdb import redisdb
from config import *


# redis连接
redis_conn = redisdb(host=HOST, db=DB, password=R_PASSWORD)
# redis_conn = redisdb(host='10.2.1.91', port=6379, db=13)

# redis连接
# redis_conn = redisdb(host='10.0.0.177', db=13, password='1qaz2wsx')


# 55mongo连接
client_55 = pymongo.MongoClient('mongodb://root:root962540@10.0.0.55:27017')
ip_results_coll = client_55['ip_db']['vps_static_ip_results']

# 本地mongo连接
client_localhost = pymongo.MongoClient('mongodb://admin:1qaz2wsx@172.16.0.64:27017')
local_all_com = client_localhost['all_com']


# 服务器mongo连接
client = pymongo.MongoClient(
        host=HOSTS,
        authSource=SOURCE,
        username=USERNAME,
        password=PASSWORD,
    )
all_com_db = client.get_database(ALL_DB,read_preference=ReadPreference.SECONDARY_PREFERRED)
all_results_coll = all_com_db.get_collection(ALL_SET, read_preference=ReadPreference.SECONDARY_PREFERRED)
all_index_results_coll = all_com_db.get_collection(ALL_INDEX_SET, read_preference=ReadPreference.SECONDARY_PREFERRED)

tyc_com_db = client.get_database(TYC_DB,read_preference=ReadPreference.SECONDARY_PREFERRED)
name_results_coll = tyc_com_db.get_collection(NAME_SET,read_preference=ReadPreference.SECONDARY_PREFERRED)
account_results_coll = tyc_com_db.get_collection(ACCOUNT_SET,read_preference=ReadPreference.SECONDARY_PREFERRED)
error_results_coll = tyc_com_db.get_collection(ERROR_SET,read_preference=ReadPreference.SECONDARY_PREFERRED)

# minglu_db = client.get_database(MINGLU_DB,read_preference=ReadPreference.SECONDARY_PREFERRED)
# tmp_qcm_index_coll = minglu_db.get_collection(TMP_QCM_SET,read_preference=ReadPreference.SECONDARY_PREFERRED)
# tmp_zy_index_coll = minglu_db.get_collection(TMP_ZY_SET,read_preference=ReadPreference.SECONDARY_PREFERRED)
# tmp_sd_index_coll = minglu_db.get_collection(TMP_SD_SET,read_preference=ReadPreference.SECONDARY_PREFERRED)



def get_usr_password():
    """
    获取账号密码
    :return: None or dict
    """
    try:
        account_info = json.loads(redis_conn.rpop('tyc_account_lists'))
    except Exception as e:
        print(e)
        return None
    return account_info



def get_name():
    """
    获取人名
    :return:None or dict
    """
    while True:
        try:
            name_info = json.loads(redis_conn.rpop('tyc_name_lists'))
            res = name_results_coll.find_one({'_id': name_info.get('_id')})
            if res.get('name_num'):
                print('已爬取')
                continue
            else:
                return name_info
        except Exception as e:
            print(e)
            one = name_results_coll.find_one({"name": {'$exists': False}})
            if one:
                time.sleep(120)
                print('缓存中暂时没有数据,120s后重试...')
            else:
                print("数据库没有符合要求的人名")
                quit()


def get_proxy(tag, log):
    """
    获取代理
    :return:list
    """
    ip_list = []
    if tag == 1:
        # ip_info = ip_results_coll.find({'flag':True})
        # for _ in ip_info:
        #     try:
        #         res = requests.get('http://www.baidu.com', proxies={"http": "http://{}".format(_.get('ip'))},timeout=5).status_code
        #         if res == 200:
        #             ip_list.append({'ip':_.get('ip'), 'mac':_.get('mac')})
        #     except Exception:
        #         log.error(_.get('mac'))
        #         continue

        ip_info = ip_results_coll.find()
        for _ in ip_info:
            ip_list.append({'ip': _.get('ip'), 'mac': _.get('mac')})
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


def insert_db(data, log):
    """
    数据入库
    :param data: 需要入库的数据列表
    :param log: 日志类
    :return:
    """
    for _ in data:
        collect_time = int(time.time() * 1000)  # 入库时间
        m = hashlib.md5(_.get('companyName').encode(encoding='utf-8'))
        change_name = m.hexdigest()
        dic = {
            "id": change_name,
            "webSource": "https://www.tianyancha.com/",
            "enterTime": {
                "updateTime": 0,
                "collectTime": str(collect_time)
            },
            "usedWeb": {
                "qichacha_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "tyc_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "qixin_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "gxzg_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "weimao_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "eqicha_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "qichamao_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "shuidi_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                },
                "zhongyi_com": {
                    "getTime": 0,
                    "state": 0,
                    "endTime": 0,
                    "flag": 0
                }
            }
        }
        dic.update(_)
        """入库逻辑：先入索引库，如果入库成功则写入当月的名录表，如果已存在则该条数据已经存在"""
        try:
            index_id = all_index_results_coll.insert_one({'_id': change_name, 'set': ALL_SET, 'flag': 0}).inserted_id
        except Exception:
            index_id = None
        finally:
            if index_id:
                try:
                    ID = all_results_coll.insert_one(dic).inserted_id
                    log.info('数据存储成功...ID:{}'.format(ID))
                except Exception as e:
                    log.error(e)
            else:
                pass
                # log.info('数据已存在...')

        """----------------------------------------------------------------"""



def redis_data():
    # import re
    # res = redis_conn.rhgetall('industry')
    # for key, value in res.items():
    with open('industry.txt','r',encoding='utf-8') as f:
        lines = f.readlines()

    data = {}
    for _ in lines:
        key ,value = _.strip().split(":")
        data[key] = value
    print(data)
    # province_list = {}
    # city_list = {}
    # for key, value in res.items():
    #     if '全部' in key.decode():
    #         province_list[key.decode()] = value.decode()
    #     else:
    #         city_list[key.decode().split('-')[1]] = value.decode()
    # area = redis_conn.rhgetall('area')
    # area_list={}
    # for key, value in area.items():
    #     # city = key.decode().split('-')[0]
    #     # city_value = city_list[city]
    #     area_list[key.decode()] = city_list[key.decode().split('-')[0]] + '&' + value.decode()
    # print(area_list)

# redis_data()
def update_db(data, log):
    """
    数据入库
    :param data: 需要入库的数据列表
    :param log: 日志类
    :return:
    """
    for _ in data:
        # collect_time = int(time.time() * 1000)  # 入库时间
        m = hashlib.md5(_.get('companyName').encode(encoding='utf-8'))
        change_name = m.hexdigest()
        # companyName = _['companyName']
        # companyUrl = _['companyUrl']
        # del _['companyName']
        # del _['companyUrl']

        res = local_all_com['rongzi_chendu'].find_one({'_id': change_name})
        if res:
            if _.get('companyTel'):
                local_all_com['rongzi_chendu'].update_one(
                    {'_id':change_name},
                    {'$set': {
                        "companyTel": _.get('companyTel',''),
                        "companyUrl": _.get('companyUrl',''),
                        "legalMan": _.get('legalMan',''),
                        "registerMoney": _.get('registerMoney',''),
                        "registerTime": _.get('registerTime',''),
                        "businessState": _.get('businessState',''),
                        "companyEmail": _.get('companyEmail',''),
                        "flag": 2
                    }}
                )
                log.info('数据更新成功...')
            else:
                log.info('没有电话')
                local_all_com['rongzi_chendu'].update_one(
                    {'_id': change_name},
                    {'$set': {
                        "flag": 3
                    }}
                )
        collect_time = int(time.time() * 1000)  # 入库时间
        companyName = _['companyName']
        companyUrl = _['companyUrl']
        dic = {
            "_id": change_name,
            "webSource": "https://www.tianyancha.com/",
            "companyName": companyName,
            "companyUrl": companyUrl,
            "docs": {
                "background": {
                    "baseInfo": _
                }
            },
            "allTime": {
                "enterTime": {
                    "updateTime": 0,
                    "collectTime": str(collect_time)
                },
                "usedWeb": {
                    "qichacha_com": {
                        "getTime": 0,
                        "state": 0,
                        "endTime": 0,
                        "flag": 0
                    },
                    "tyc_com": {
                        "getTime": 0,
                        "state": 0,
                        "endTime": 0,
                        "flag": 0
                    },
                    "qixin_com": {
                        "getTime": 0,
                        "state": 0,
                        "endTime": 0,
                        "flag": 0
                    },
                    "gxzg_com": {
                        "getTime": 0,
                        "state": 0,
                        "endTime": 0,
                        "flag": 0
                    },
                    "weimao_com": {
                        "getTime": 0,
                        "state": 0,
                        "endTime": 0,
                        "flag": 0
                    },
                    "eqicha_com": {
                        "getTime": 0,
                        "state": 0,
                        "endTime": 0,
                        "flag": 0
                    }
                }
            },
            'reportFlag': 0,
            'flag': 0,
        }
        try:
            all_results_coll.insert_one(dic)
            # tmp_zy_index_coll.insert_one({'_id': dic.get('_id'), 'companyName': dic.get('companyName')})
            log.info('数据存储成功...')
        except Exception as e:
            log.info('数据已存在...')
            pass


# if __name__ == '__main__':
    redis_data()