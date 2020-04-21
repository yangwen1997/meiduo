import xlrd
import os
import time
import pymongo
import hashlib
import threading, queue

excpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/exc"  # 指定根目录
# 获取指定路径下的文件
file_dirs = os.listdir(excpath)
print('[INFO]: excel总数：{}'.format(len(file_dirs)))
fileQueue = queue.Queue()
for file_name in file_dirs:
        file_info = '{}/{}'.format(excpath, file_name)
        fileQueue.put(file_info)

"""
批量导出名录数据写入数据库（excel表格）
"""
def excel_parse(fileQueue, db):
    header_dic = {
        '公司名称': 'companyName',
        '法定代表人': 'legalMan',
        '注册资本': 'registerMoney',
        '成立日期': 'registerTime',
        '企业公示的联系电话': 'companyTel',
        '企业公示的地址': 'registerAddress',
        '企业公示的网址': 'companyWebeUrl',
        '企业公示的邮箱': 'companyEmail',
        '经营范围': 'businessScope',
        '所属地区': 'companyProvince',
        '统一信用代码': 'creditCode',
    }
    while True:
        try:
            # 不阻塞的读取队列数据
            file_info = fileQueue.get_nowait()
            print(file_info)
            i = fileQueue.qsize()
        except Exception as e:
            break
        print('Current Thread Name %s, Url: %s ' % (threading.currentThread().name, file_info))
        """读取excel表格"""
        workbook = xlrd.open_workbook(file_info)
        print(workbook)
        # 定位到sheet1
        worksheet1 = workbook.sheet_by_name(workbook.sheet_names()[0])
        print('worksheet1 is %s' % worksheet1)
        # 遍历sheet1中所有行row
        num_rows = worksheet1.nrows
        for curr_row in range(num_rows):
            # 跳过第一行
            if curr_row == 0:
                continue
            # 跳过第二行
            elif curr_row == 1:
                list_header = worksheet1.row_values(curr_row)
                # print(list_header)
            else:
                list_row = worksheet1.row_values(curr_row)
                print('row%s is %s' % (curr_row, list_row))

                """数据入库"""
                dic = {}
                for name, value in header_dic.items():
                    dic[value] = list_row[list_header.index(name)]
                    print("[INFO]: {}：{}".format(name, dic[value]))
                companyName = dic['companyName']
                del dic['companyName']
                m = hashlib.md5(companyName.encode(encoding='utf-8'))
                change_name = m.hexdigest()
                collect_time = int(time.time() * 1000)  # 入库时间
                data = {
                    "_id": change_name,
                    # 公司名称
                    "companyName": companyName,
                    # 公司链接
                    "companyUrl": '',
                    # 详情
                    "docs": {
                        "background": {
                            "baseInfo": dic
                        }
                    },
                    # 名录来源网址
                    "webSource": "https://www.tianyancha.com/",
                    # 时间
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
                    'reportFlag': 0
                }
                try:
                    db["all_results"].insert_one(data)
                    print("[INFO]: 数据存储中...\n")
                except Exception as e:
                    print(e)
                    print("[INFO]: 数据已经存在,正在过滤中...\n")


if __name__ == '__main__':
    client = pymongo.MongoClient(
        'mongodb://rwuser:48bb67d7996f327b@10.0.0.120:57017,10.0.0.121:57017,10.0.0.122:57017/?replicaSet=rs1')
    db = client["all_com"]
    startTime = time.time()
    threads = []
    # 设置线程数
    threadNum = 20
    for i in range(0, threadNum):
        t = threading.Thread(target=excel_parse, args=(fileQueue,db,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
        t.join()
    endTime = time.time()
    print('Done, Time cost: %s ' % (endTime - startTime))
