import requests
import re
from cookiespool.db import AccountRedisClient
domain ='account'   # 账号
# domain = 'cookies' # cookie
name = 'sooip'      # sooip网站
# name = 'cnipr'    # cnipr网站

# 实例化redis连接
conn = AccountRedisClient(name=name,domain=domain)


def read_account(filename):
    """
    从text获取账号密码信息
    :param filename: 文件名
    :return:
    """
    with open(filename, 'r') as f:
        res = f.readlines()
        r = [r.strip() for r in res]
        account_dict = {}
        for account in r:
            x = account.replace('\t', '-').replace(' ', '-')
            data = x.split('-')
            username = data[0]
            password = data[-1]
            account_dict[username] = password
        return account_dict


def set(username, password):
    """
    账号密码写入redis
    :param username:
    :param password:
    :return:
    """
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


if __name__ == '__main__':
    account_dict = read_account('account_sooip.txt')
    for key, value in account_dict.items():
        set(key, value)
    print('录入完成')
