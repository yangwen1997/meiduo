'''
@author: 杨文龙
@file : run.py
@time: 2019/5/29
@desc:
'''

#进程/线程/协程
import multiprocessing
import threadpool
import asyncio
from random import choice
import requests
from fake_useragent import UserAgent
ua = UserAgent()

#本地

#两种方法

#动态IP
from wens.wenshu import WENS
#静态IP
# from wens.redis_docid import WENS


from wens.common import get_proxy
from wens.common import REDIS
from wens.get_ip import GetIP


red_cli = REDIS


def check_ip():
    """
    获取IP
    :return:
    """
    # IP = GetIP()
    while 1:
        # pro = IP.get_jt()
        # prox = eval(pro)["ip"]

        prox = choice(get_proxy(1))["ip"]
        proxy = {
            "http": "http://" + prox, "https": "https://" + prox,
        }
        check_pro = {"ip": proxy["http"]}
        tag = red_cli.sismember("wenshu_bad_ip", str(check_pro))



        if tag:
            print("该IP存在失效IP池中，不能使用")
        else:
            return proxy

def func():
    """
    开启的进程（线程）
    :return:
    """

    count = red_cli.scard("wenshu_search")
    while count:
        try:
            name = red_cli.srandmember("wenshu_search")
            search = "全文检索:{}".format(eval(name)["search_name"])

            proxy = check_ip()
            wen = WENS(proxy=proxy,search=search)
            TAG = wen.run()

            if TAG:
                count -= 1
                red_cli.srem("wenshu_search",name)
            else:
                pass

        except:
            pass


async def func_1():
    """
    协程1号
    :return:
    """
    pass

async def func_2():
    """
    协程2号
    :return:
    """
    pass

def asy():
    """
    异步协程asynico,协程不可以在线程池中开启，可以在进程中直接挂载
    :return:
    """

    #创建事件循环
    loop = asyncio.get_event_loop()

    #开启异步协程任务
    tasks = [
        loop.create_task(func_1()),
        loop.create_task(func_2()),
    ]

    #开启协程并等待执行完毕
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

def thr():
    """
    使用线程池
    :return:
    """
    pool = threadpool.ThreadPool(10)
    name_list = ["1号线程","2号线程","3号线程","4号线程","5号线程"]
    req = threadpool.makeRequests(func,name_list)
    [pool.putRequest(_)for _ in req]
    pool.wait()

def pro():
    """
    使用cpu异步挂载进程
    :return:
    """
    pool = multiprocessing.Pool(11)

    for _ in range(10):
        pool.apply_async(func)

        #使用进程加协程
        # pool.apply_async(asy)
    pool.close()
    pool.join()

def main():
    """
    程序开始函数，选择进程（协程或者线程）启动
    :return:
    """
    pro()


if __name__ == '__main__':
    main()