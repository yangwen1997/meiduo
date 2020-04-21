import time
from multiprocessing import Process

from cookiespool.api import app
from CookiesPool.config import *
from cookiespool.generator import *
from cookiespool.tester import *


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=VALID_CYCLE):
        """
        验证器，循环检测数据库中Cookies是否可用，不可用删除
        :param cycle: 间隔时间
        :return:
        """
        while True:
            print('Checking Cookies')
            try:

                for name, cls in TESTER_MAP.items():
                    tester = eval(cls + '(name="' + name + '")')
                    tester.run()
                    print('Tester Finished')
                    del tester
                time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=GEN_CYCLE):
        """
        产生器，模拟登录添加Cookies
        :param cycle: 间隔时间
        :return:
        """
        while True:
            print('Generating Cookies')
            try:
                for name, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(name="' + name + '")')
                    generator.run()
                    print('Generator Finished')
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        app.run(host=API_HOST, port=API_PORT, threaded=True)

    def run(self):
        """
        程序入口
        :return:
        """
        # 产生器，模拟登录添加Cookies
        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()
        # 验证器，循环检测数据库中Cookies是否可用，不可用删除
        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()
        # API接口服务
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

