#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019/1/4 16:48
@Author  : 方甜
@File    : second_program_company_spider.py
@Software: PyCharm
@Version : 1.0
@Desc    : 第二套方案抓取名录（重构版）
"""
import math, re, json, hashlib, urllib.parse, time, requests, datetime
import rk_python3
from gevent import sleep
# from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as B
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image,ImageFont, ImageDraw
from slide_recognition import SlideRecognition
from common import redis_conn, name_results_coll, account_results_coll,\
    insert_db,error_results_coll,DuplicateKeyError,ip_results_coll
chrome_options = webdriver.ChromeOptions()
class CompanySpider(object):
    """
    第二套方案抓取名录方案
    """
    def __init__(self, img_path, count, ip_dic, proxy_tag, log):
        """
        参数初始化
        :param img_path:验证码图片存储路径
        :param ip_dic: 代理信息的字典（包含ip,mac）
        :param count: 启动chrome时的延迟时间
        :param proxy_tag: IP代理的方式，proxy_tag==1(使用静态代理),proxy_tag==2(使用香港代理)
        :param log: 日志类
        :type proxy_tag:int
        """
        # 日志
        self.log = log
        # 登陆链接
        self.login_url = "https://www.tianyancha.com/login"
        # 省份和城市的参数
        data  = self.get_city()
        self.province_dic = data.get('province')
        self.city_dic = data.get('city')
        # 地区的参数
        self.area_dic = self.get_area()
        # 图片存储路径
        self.img_path = img_path
        print(self.img_path)
        # 数据存储列表
        self.data = []
        # IP代理的方式
        self.proxy_tag = proxy_tag
        if self.proxy_tag == 1:
            # ip的mac
            self.mac = ip_dic.get('mac')
            # 代理IP
            self.ip = ip_dic.get('ip')
            self.log.info('IP is: {}'.format(self.ip))
        else:
            self.ip = ip_dic
        self.driver = None
        # 延时时间
        self.count = count
        # 验证码图片标号
        self.skip_count = count
        # 实例化driver
        self.chrome_driver()
        # 实例化滑块验证码类
        self.code = SlideRecognition()

    def switch_ip(self):
        """
        更换代理
        :return:
        """
        while True:
            res = ip_results_coll.find_one({'mac': self.mac})
            if res.get('flag'):
                try:
                    resp = requests.get('http://www.baidu.com', proxies={
                        "http": "http://{}".format(res.get('ip'))},
                                       timeout=20).status_code
                    if resp == 200:
                        self.ip = res.get('ip')
                        self.log.info('IP is: {}'.format(self.ip))
                        break
                except Exception:
                    self.log('IP超时...')
                    continue
            else:
                self.log.info('正在获取IP, 30后重试...')
                sleep(30)

    def dial_ip(self):
        """
        代理拨号
        :return:
        """
        try:
            ip_results_coll.update_one({'mac':self.mac}, {'$set': {'flag': False}})
            self.log.info('IP：拨号中....')
        except Exception as e:
            self.log.error(e)

    def chrome_driver(self):
        """
        实例化driver
        :return:
        """
        # 启动延时时间
        sleep_time = self.count*5
        self.log.info('延时{}s启动...'.format(sleep_time))
        sleep(sleep_time)
        # driver配置
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('-no-sandbox')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument('--disable-plugins-discovery')

        # 如果proxy_tag==1使用下面的配置方式，否则使用else下的配置方式
        if self.proxy_tag == 1:
            chrome_options.add_argument("--proxy-server=http://{}".format(self.ip))
            desired_capabilities = None
        else:

            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            desired_capabilities['proxy'] = {
                "httpsProxy": self.ip,
                # "ftpProxy": PROXY,
                # "sslProxy": PROXY,
                "noProxy": None,
                "proxyType": "DIRECT",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
        # 实例化driver
        self.driver = webdriver.Chrome(
            # executable_path='D:\software\chromedrive\chromedriver.exe',
            chrome_options=chrome_options,
            desired_capabilities=desired_capabilities)
        # 设置页面等待超时时间（由于代理网络有时延时较高，所以设置等待超时时间为40s）
        self.driver.set_page_load_timeout(40)

    def run(self):
        """
        主程序入口
        :return:
        """
        # try:
        # 账号信息
        self.account_info = self.get_account_from_redis()
        # 登陆
        self.login()
        # 获取人名
        while True:
            self.name_info = self.get_name_from_redis()
            if self.name_info:
                # 姓名进行编码转换
                self.log.info("正在获取人名详情：{}".format(self.name_info['name']))
                self.label_name = urllib.parse.quote(self.name_info['name'])
                url = self.url_config(key=self.label_name)
                # 请求页面
                while True:
                    status = self.search_detail(url)
                    company_num = self.logic_detail('search', status)
                    if str(company_num).isdigit():
                        self.log.info('公司总数：{}'.format(company_num))
                        self.judge_num(company_num)
                    elif company_num is False:
                        continue
                    break
                # 判断是否改名字下是否有数据
                if self.data:
                    # 入库
                    insert_db(self.data, self.log)
                    # 修改标记位
                    collection = {'_id': self.name_info['name_id']}
                    query = {'$set': {'flag': 1}}
                    self.update_database_status('name', collection, query)
                    # 重新实例化数据存储列表
                    self.data = []
                print("-----------------\n")
            else:
                return
        # except Exception as e:
        #     self.log.error(e)
        #     self.driver.quit()

    def url_config(self, **kwargs):
        """
        url添加条件参数
        ep:condition = '/or100200-e015' # 注册资本100万到200万并且成立时间1-5年
           condition = '/oe510' # 成立时间5-10年
           condition = '/or0100' # 注册资本0-100万
           base = '&base=heb' # 河北省
           base = '&base=qhd' # 秦皇岛市
           area_code = '&areaCode=130304' # 北戴河区

        :param condition: 注册资本和注册时间的参数
        :param key: 搜索的名称参数（url编码后的）
        :param base: 省份或者城市的参数
        :param area_code: 地区的参数
        :return: 返回拼接后的参数

        """
        # ep: https://www.tianyancha.com/search/or0100-e01?key=%E5%B0%8F%E8%B4%9D&base=bj&areaCode=110101'
        return 'https://www.tianyancha.com/search{}?key={}{}{}'.format(
            kwargs.setdefault('condition',''),
            kwargs.setdefault('key', ''),
            kwargs.setdefault('base', ''),
            kwargs.setdefault('area_code', ''))


    def login(self):
        """
        登陆模块
        :return:
        """
        # 需要重新登陆标记位
        status = False
        # 获取账号信息
        while not status:
            try:
                # 设置窗口大小
                self.driver.set_window_size(900, 1000)
                self.driver.get(self.login_url)
                sleep(2)
                self.log.info('正在使用账号: {}'.format(self.account_info.get('account_name')))
                cookies = self.get_cookie_from_redis()
                if cookies:
                    self.driver.delete_all_cookies()
                    for _ in cookies:
                        self.driver.add_cookie(_)
                    self.driver.get("https://www.tianyancha.com/")
                else:
                    # 点击密码登陆
                    self.driver.find_element_by_xpath("//div[@onclick='changeCurrent(1);']").click()
                    # js填充账号和密码
                    js_str = """document.querySelector(".mobile_box .contactphone").value = '{}';document.querySelector(".mobile_box .contactword").value = '{}';document.querySelectorAll('.btn.-hg.btn-primary.-block')[2].click()""".format(self.account_info['account_name'], self.account_info['password'])
                    self.driver.execute_script(js_str)
                if '手机号码密码错误' in self.driver.page_source or '我们只是确认一下你不是机器人' in self.driver.page_source:
                    # 打码失败
                    updateTime = str(int(time.time() * 1000))
                    account_results_coll.update_one(
                        {'_id': self.account_info['account_id']},
                        {'$set': {"usable": 1, 'updateTime': updateTime}}
                    )
                    # 账号信息
                    self.account_info = self.get_account_from_redis()
                    status = False
                else:
                    # 检测是否登陆成功
                    status = self.check_question('login')
            except Exception as e:
                # try:
                #     self.log.error("页面加载超时, ERROR:{}".format(e))
                #     if 'CONNECTION' in self.driver.page_source or ('timeout' in str(e)):
                #         # 如果是网络问题或者超时，则重新更换代理IP然后重启driver
                #         self.driver.close()
                #         self.driver.quit()
                #         # 切换代理
                #         self.switch_ip()
                #         # 实例化driver
                #         self.chrome_driver()
                #         sleep(5)
                #     elif '天眼查' not in self.driver.page_source:
                #         # 重新拨号
                #         self.dial_ip()
                #     else:
                #         self.driver.refresh()
                # except Exception as e:
                #     self.log.error(e)
                self.log.error("页面加载超时, ERROR:{}".format(e))
                try:
                    self.driver.refresh()
                except Exception as e:
                    self.log.error(e)
                # 如果是网络问题或者超时，则重新更换代理IP然后重启driver
                self.driver.close()
                self.driver.quit()
                # 切换代理
                self.switch_ip()
                # 实例化driver
                self.chrome_driver()
                sleep(5)
                status = False
                continue

            # 修改数据库状态，如果status==True表示登陆成功，将标记为改位flag:1,否则表示登陆失败，账号不可用，将usable改位1
            condition = {'_id': self.account_info['account_id']}
            update_tag = 'account'
            query = {'$set': {'flag': 1}} if status else {'$set': {'usable': 1}}
            self.update_database_status(update_tag, condition, query)

    def get_name_from_redis(self):
        """
        获取搜索队列模块
        :return:返回姓名信息包括_id,name
        :rtype:dict or None
        """
        while True:
            # 从姓名队列获取一条数据
            try:
                name_info = json.loads(redis_conn.rpop('tyc_name_lists').decode())
                # 去数据库查询该条数据
                res = name_results_coll.find_one({'_id': name_info['_id']})
                # 如果flag !=0 表示已经抓取过，重新获取一条数据
                if res.get('flag'):
                    print('已爬取')
                    continue
            except Exception as e:
                self.log.error("数据库查询人名失败, ERROR:{}".format(e))
                time.sleep(30)
                continue
            # 如果数据存在返回信息(_id,name)
            if name_info:
                self.log.info("姓名：{}".format(name_info['name']))
                if  len(name_info['name']) > 3:
                    # 修改标记位(不能爬取)
                    collection = {'_id': name_info['_id']}
                    query = {'$set': {'flag': 3}}
                    self.update_database_status('name', collection, query)
                    continue
                return {
                    'name_id':name_info['_id'],
                    'name':name_info['name'],
                }
            else:
                # 查询条件，跟写入姓名队列的查询条件一致
                query = {
                    'company_numm': {'$lte': 100, '$gt': 0},
                    'flag': {'$ne': 1}
                }
                one = name_results_coll.find_one(query)
                # 如果有数据说名队列补充还没有完成,等一分钟后重试，否则表示该条件下的姓名已经抓取完成，程序结束
                if one:
                    sleep(60)
                    self.log.info('缓存中暂时没有数据,60s后重试...')
                    continue
                else:
                    self.log.info("数据库没有符合要求的人名")
                    self.driver.quit()
            # return {
            #     'name_id': '125d500bd6ce88213174b699ee40481',
            #     'name': '岳池县武忠"郎"牌原浆酒专卖店',
            # }


    def get_account_from_redis(self):
        """
        获取账号队列模块
        :return:返回账号信息（_id, 账号, 密码）
        :rtype:dict
        """
        while True:
            # 从队列获取一条账号信息，如果失败获取次数减1，从新获取直到获取成功
            try:
                account_info = json.loads(
                    redis_conn.rpop('tyc_account_lists').decode())
            except Exception as e:
                self.log.error(e)
                self.log.error("数据库没有符合要求的账号或者redis出现错误, ERROR:{}".format(e))
                sleep(10)
                continue
            # 如果获取到账号信息则返回 _id, 账号, 密码
            if account_info:
                return {
                    'account_id': account_info['_id'],
                    'account_name': account_info['account_name'],
                    'password': account_info['password'],
                }
            # return {
            #     'account_id': 'c39a30f96ccd9cb9e5e2bd77da4ce7c5',
            #     'account_name': 15943503545,
            #     'password': 'a123456789',
            # }

    def search_detail(self, url):
        """
        搜索模块
        :param url: 请求链接
        :return: status返回请求状态，正常：返回搜索到的公司数量，搜索不到结果返回True,出现验证码返回False,其他异常返回
        """
        # 重试次数
        retry_count = 0
        while True:
            # 请求处理
            try:
                # 设置窗口大小
                self.driver.set_window_size(400, 600)
                self.driver.get(url)
                self.log.info(url)
                sleep(3)
            except Exception as e:
                self.log.info(e)
                sleep(3)
                try:
                    self.driver.refresh()
                except Exception:
                    self.dial_ip()
                    sleep(3)
                continue
            # 如果是网路问题则切换代理重新实例化driver,再重新登陆
            if 'CONNECTION' in self.driver.page_source or '天眼查' not in self.driver.page_source:
                self.driver.close()
                self.driver.quit()
                self.log.info('切换IP')
                # 更换代理
                self.switch_ip()
                self.log.info('重新实例化driver')
                # 实例化driver
                self.chrome_driver()
                # 重新登陆
                self.login()
                time.sleep(5)
                retry_count += 1
                self.log.info('当前第{}次重试'.format(retry_count))
                continue
            # elif '天眼查' not in self.driver.page_source:
            #     self.log.info('当前页面为空，去重新拨号...')
            #     self.dial_ip()
            #     sleep(3)
            #     continue
            else:
                # 检测跳转页面是否正常
                try:
                    status = self.check_question('search')
                except Exception as e:
                    self.log.error('ERROR2: {}'.format(e))
                    continue
                return status


    def logic_detail(self, tag, status):
        """
        搜索页面后的处理逻辑
        :param tag:  搜索的类型（姓名的搜索，添加条件的搜索，翻页的请求）
        :param status: 搜索返回的状态（int: 正常返回, False: 账号需要打码, True: 没有搜索到结果, None：可能是网络问题或其他未知异常）
        :return: 搜索到的公司数量或者False或者None
        """
        if str(status).isdigit():
            # 正常请求
            return status
        elif status is False:
            # 账号需要打码
            self.image_handle()
            if ('我们只是确认一下你不是机器人' in self.driver.page_source) or ('登录/注册' in self.driver.page_source):
                collection = {'_id': self.account_info['account_id']}
                updateTime = str(int(time.time() * 1000))
                query = {'$set': {"flag": 2, 'updateTime': updateTime}}
                self.update_database_status('account', collection, query)
            else:
                collection = {'_id': self.account_info['account_id']}
                updateTime = str(int(time.time() * 1000))
                query = {'$set': {"flag": 10, 'updateTime': updateTime}}
                self.update_database_status('account', collection, query)
            # 重新登陆
            # 删除cookie
            redis_conn.rhdel('login_cookies', self.account_info['account_name'])
            self.account_info = self.get_account_from_redis()
            self.driver.close()
            self.driver.quit()
            self.log.info('切换IP')
            # 重新拨号
            self.dial_ip()
            # 更换代理
            self.switch_ip()
            self.log.info('重新实例化driver')
            # 实例化driver
            self.chrome_driver()
            # self.driver.delete_all_cookies()
            sleep(3)
            self.login()
            return False
        elif status is True:
            if tag == 'search':
                # 没有搜索到结果,修改姓名表的标记位
                collection = {'_id': self.name_info['name_id']}
                query = {
                    '$set':
                        {"name_num": 0, "company_numm": 0, 'flag': 4}
                }
                self.update_database_status('name', collection, query)
            else:
                # 其他情况不做处理
                pass
        else:
            # 记录请求错误的url到数据库
            collection = self.name_info
            collection['url'] = self.driver.current_url
            self.update_database_status('error', collection)

    def check_question(self, check_tag):
        """
        异常处理模块
        :param check_tag: 异常检测类型
        :return:
        """
        # 检测是不是网络问题，如果是过一段时间刷新一下
        count = 3
        while count:
            if 'proxy' in self.driver.page_source:
                self.log.info('网络不稳定, 30s后重试...')
                self.driver.refresh()
                sleep(30)
                count -=1
            else:
                break
        if check_tag == 'login':
            # 查看是否登陆成功
            while True:
                sleep(3)
                # 点击登录，成功直接跳转首页
                try:
                    self.driver.find_element_by_xpath(
                        "//div[@class='module module1 module2 loginmodule collapse in']/div/div[5]").click()
                except Exception:
                    pass
                try:
                    home_pages = self.driver.find_element_by_xpath("//input[@id='home-main-search']")
                    self.cookie_to_redis()
                except Exception:
                    if '关闭验证重试' in self.driver.page_source:
                        try:
                            self.driver.refresh()
                        except Exception:
                            pass
                    elif '请先完成下方验证' in self.driver.page_source:
                        self.log.error('验证码没有通过...重试...')
                        self.code.image_handle(self.driver)
                        continue
                    home_pages = None
                break
            # 如果跳转到首页即登录成功
            if home_pages:
                return True
            else:
                return False
        elif check_tag == 'search':
            try:
                content = self.driver.find_element_by_xpath('//span[contains(text(),"天眼查为你找到")]/..').text
                match = int(re.search(r'天眼查为你找到(\d+)\+?家公司', content).group(1))
                return match
            except Exception as e:
                if "抱歉，没有找到相关结果！" in self.driver.page_source:
                    return True
                # 检测是不是跳转到验证码页面
                elif '我们只是确认一下你不是机器人' in self.driver.page_source:
                    return False
                else:
                    self.log.error('搜索页得其他错误, ERROR:{}'.format(e))
                    return None

    def cookie_to_redis(self):
        """
        登陆过后的cookies处理
        :return:
        """
        cookie_dic = [{'name': cookie['name'], 'value': cookie['value']} for cookie in self.driver.get_cookies()]
        redis_conn.rhset('login_cookies', self.account_info['account_name'],json.dumps(cookie_dic))

    def get_cookie_from_redis(self):
        if redis_conn.rhexists('login_cookies', self.account_info['account_name']):
            return json.loads(redis_conn.rhget('login_cookies', self.account_info['account_name']).decode())

    def judge_num(self, num):
        """
        根据公司数量进行下一步处理
        :param num: 公司数量
        :return:
        """
        if num <=100:
            self.page_detail(num)
        elif 100 < num <= 500:
            # 资本条件
            self.money_condition()
        elif 500 < num <= 6000:
            # 省份条件
            self.province_condition()
        elif 6000 < num <= 35000:
            # 城市条件
            self.city_condition()
        else:
            # 地区条件
            self.area_condition()

    def money_condition(self, **kwargs):
        """
        资本条件
        :param base:城市或者省份参数
        :param area_code:地区参数
        :return:
        """
        money_condition = ['r0100', 'r100200', 'r200500', 'r5001000', 'r1000']
        for _ in money_condition:
            parameter = '/o{}'.format(_)
            url = self.url_config(
                key=self.label_name,
                condition=parameter,
                **kwargs)
            while True:
                status = self.search_detail(url)
                company_num = self.logic_detail('condition',status)
                if str(company_num).isdigit():
                    if company_num > 100:
                        self.time_condition(_, **kwargs)
                    else:
                        self.page_detail(company_num)
                elif company_num is False:
                    continue
                break

    def time_condition(self, money_condition, **kwargs):
        """
        时间条件
        :param money_condition:注册资本的参数
        :param base:城市或者省份参数
        :param area_code:地区参数
        :return:
        """
        time_condition = ['e01', 'e015', 'e510', 'e1015', 'e15']
        for _ in time_condition:
            parameter = '/o{}-{}'.format(money_condition, _)
            url = self.url_config(
                key=self.label_name,
                condition=parameter,
                **kwargs)
            while True:
                status = self.search_detail(url)
                company_num = self.logic_detail('condition', status)
                if str(company_num).isdigit():
                    if company_num > 100:
                        # 数量还是大于100的记录到数据库
                        pass
                    else:
                        self.page_detail(company_num)
                elif company_num is False:
                    continue
                break

    def province_condition(self):
        """
        省份条件
        :return:
        """
        for key, value in self.province_dic.items():
            pro_parameter = '&{}'.format(value)
            url = self.url_config(key=self.label_name, base=pro_parameter)
            while True:
                status = self.search_detail(url)
                company_num = self.logic_detail('condition', status)
                if str(company_num).isdigit():
                    self.log.info('{} 公司数量: {}'.format(key, company_num))
                    if company_num > 100:
                        self.money_condition(base=pro_parameter)
                    else:
                        self.page_detail(company_num)
                elif company_num is False:
                    continue
                break

    def city_condition(self):
        """
        城市条件
        :param num:公司数量
        :return:
        """
        for key, value in self.city_dic.items():
            city_parameter = '&{}'.format(value)
            url = self.url_config(key=self.label_name, base=city_parameter)
            while True:
                status = self.search_detail(url)
                company_num = self.logic_detail('condition', status)
                if str(company_num).isdigit():
                    self.log.info('{} 公司数量: {}'.format(key, company_num))
                    if company_num > 100:
                        self.money_condition(base=city_parameter)
                    else:
                        self.page_detail(company_num)
                elif company_num is False:
                    continue
                break

    def area_condition(self):
        """
        地区条件
        :return:
        """
        for key, value in self.area_dic.items():
            area_parameter = '&{}'.format(value.get('area_code'))
            city_parameter = '&{}'.format(value.get('base'))
            url = self.url_config(
                key=self.label_name,
                base=city_parameter,
                area_code=area_parameter)
            while True:
                status = self.search_detail(url)
                company_num = self.logic_detail('condition', status)
                if str(company_num).isdigit():
                    self.log.info('{} 公司数量: {}'.format(key, company_num))
                    if company_num > 100:
                        self.money_condition(
                            base=city_parameter,
                            area_code=area_parameter)
                    else:
                        self.page_detail(company_num)
                elif company_num is False:
                    continue
                break

    def html_detail(self):
        """
        解析模块,解析列表页面
        :return: 解析后的数据
        :rtype:dict or None
        """
        """另一种策略,不具体定位class里面的值，因为class里面的值会变，所以定位到标签，再用正则做匹配"""
        try:
            # 获取页面html
            html = B(self.driver.page_source, 'html.parser')
            # 找到所有的公司外层的模块
            # div_lists = html.find_all('div', attrs={'data-id': re.compile('\d+')})
            div_lists = html.find('div', class_='result-list sv-search-container').find_all(
                'div', attrs={'data-id': re.compile('\d+')})
        except Exception as e:
            self.log.error('找不到所有的公司外层的模块{}'.format(e))
            return

        items = []

        for div in div_lists:
            dic = {}
            # 基本信息json
            try:
                base_txt = str(div.find('span', class_='tt hidden').get_text())
            except Exception:
                base_txt = None
            # 找不到基本信息的json，可能是事业单位这种类型的，走下面那个逻辑
            if base_txt:
                # 基本信息字典
                base_txt = base_txt.replace('\"\"','None').replace('\'', '\"').replace('null','None').replace('true', 'True')
                try:
                    base_dic = self.re_sub(base_txt)
                except Exception:
                    base_txt = base_txt.replace('\"\"','None').replace('\'', '\"').replace('null','None').replace('true', 'True')
                    base_dic = eval(base_txt)
                # 公司名称
                dic['companyName'] = base_dic.get('name')
                # 公司url
                dic['companyUrl'] = "https://www.tianyancha.com/company/{}".format(base_dic.get('id'))
                # 营业状态
                dic['businessState'] = base_dic.get('regStatus')
                # 省份
                dic['companyProvince'] = base_dic.get('base')
                # 注册资金
                dic['registerMoney'] = base_dic.get('regCapital')
                # 注册时间
                dic['registerTime'] = base_dic.get('estiblishTime').split(' ')[0]
                # 联系电话
                dic['companyTel'] = base_dic['phoneList'] if base_dic.get('phoneList') else ''
                # 邮箱
                dic['companyEmail'] = base_dic.get('emailList') if base_dic.get('emailList') else ''
                # 统一信用代码
                dic['creditCode'] = base_dic.get('creditCode')
                # 注册地址
                dic['registerAddress'] = base_dic.get('regLocation')
                # 经营范围
                dic['businessScope'] = base_dic.get('businessScope')
                # 所属行业
                dic['industry'] = base_dic.get('categoryStr')
                # 所属城市
                dic['companyCity'] = base_dic.get('city')
                # 所属地区
                dic['companyArea'] = base_dic.get('district')
                # 基本信息json
                dic['base_txt'] = base_txt
            else:
                try:
                    tmp = div.find('a', attrs={
                        'href': re.compile('https://www.tianyancha.com/company/\d+')})
                    # 公司名称
                    dic['companyName'] = tmp.get_text(strip=True)
                    # 公司url
                    dic['companyUrl'] = tmp.attrs['href']
                except Exception as e:
                    self.log.error(e)
                    continue
                # 经营状态
                try:
                    dic['businessState'] = tmp.next_sibling.get_text(strip=True)
                except Exception:
                    dic['businessState'] = ''
                # 公司所属省份
                try:
                    dic['companyProvince'] = div.contents[3].get_text(strip=True)
                except Exception:
                    dic['companyProvince'] = ''

                # 法人/注册资本/注册时间/联系电话/邮箱/法人信息
                tags = div.contents[2].contents[1:-1]
                data = []
                for tag in tags:
                    for _ in tag.contents:
                        data.append(_.get_text(strip=True))
                # 对初步解析的文本进一步分割
                tmp_dic = {'法定代表人': 'legalMan',
                           '代表人': 'representMan',
                           '负责人': 'chargeMan',
                           '注册资本': 'registerMoney',
                           '资本总额': 'registerMoney',
                           '注册时间': 'registerTime',
                           '联系电话': 'companyTel',
                           '邮箱': 'companyEmail',
                           }
                for _ in data:
                    try:
                        key, value = _.split("：")
                    except Exception:
                        continue
                    # 联系电话可能存在多个
                    if key in ['法定代表人', '代表人', '负责人']:
                        # 法定代表人url
                        try:
                            dic['manUrl'] = \
                            div.find('a', attrs={'title': value}).attrs['href']
                        except Exception:
                            pass
                            # log.error('获取法人链接失败')
                    if key in ['联系电话', '邮箱']:
                        try:
                            tel_lists = re.search(
                                '.*\[(.*)\].*',
                                value.replace('\"', '')
                            ).group(1).split(',')
                        except Exception:
                            tel_lists = [value]
                        dic[tmp_dic[key]] = tel_lists
                    else:
                        try:
                            dic[tmp_dic[key]] = value
                        except Exception:
                            pass
            # 数据存储
            items.append(dic)
        return items if items else None

    def re_sub(self, base_txt):
        """
        字典提取
        :param base_txt: 需要匹配的文本
        :return:
        """
        key_list = [
            'phoneList',
            'emailList',
            'id',
            'name',
            'regStatus',
            'base',
            'regCapital',
            'estiblishTime',
            'creditCode',
            'regLocation',
            'businessScope',
            'categoryStr',
            'city',
            'district',
        ]

        data = {}
        for _ in key_list:
            pattern = r'"{}":"?(.*?\"?.*?\"?.*?)"?,'.format(_)
            data[_] = re.search(pattern, base_txt).group(1)

        em_list = re.search(
            r'"emails":"?(.*?\"?.*?\"?.*?)"?,"emailList"',
            base_txt
        ).group(1).replace("\\t", '').split(';')
        data['emailList'] = [x for x in em_list if x != '' and x != 'None']
        ph_list = re.search(
            r'"phoneNum":"?(.*?\"?.*?\"?.*?)"?,"phoneList"',
            base_txt
        ).group(1).replace("\\t", '').split(';')
        data['phoneList'] = [x for x in ph_list if x != '' and x != 'None']
        return data

    def page_detail(self, num):
        """
        翻页处理模块
        :param num: 搜索到的公司数量
        :return:
        """
        # 计算总页数( 向上取整)
        company_page = math.ceil(num / 20)
        # 当前请求的url
        url = self.driver.current_url
        for next_link in range(1, int(company_page) + 1):
            # 如果不是第一页需要拼接翻页参数获取新的url请求翻页页面，否则直接解析页面
            if next_link != 1:
                # 翻页的参数
                page_condition = '/p{}?'.format(next_link)
                # 重新拼接url
                page_url = url.replace('?', page_condition)
                while True:
                    # url请求
                    status = self.search_detail(page_url)
                    # 请求过后的逻辑处理
                    company_num = self.logic_detail('page', status)
                    # 网络问题重新请求
                    if company_num is False:
                        continue
                    break
            # 解析页面
            item = self.html_detail()
            # 如果有数据添加到数据存储列表中
            if item:
                self.data.extend(item)

    def update_database_status(self, update_tag, condition, query=None):
        """
        修改数据库状态模块
        :param update_tag: 对应的数据库
        :param condition: 需要修改的_id
        :param query: 需要修改的条件
        :return:
        """
        db_dic =  {
            'name': name_results_coll,
            'account': account_results_coll,
            'error': error_results_coll,
        }
        if update_tag == 'error':
            data = {
                '_id': self.to_md5(condition['url']),
                'name_id': condition['name_id'],
                'name': condition['name'],
                'url': condition['url']
            }
            while True:
                try:
                    db_dic[update_tag].insert_one(data)
                    break
                except DuplicateKeyError:
                    break
                else:
                    continue
        else:
            db_dic[update_tag].update_one(condition, query)

    def get_city(self):
        """
        从缓存中读取城市和省份的参数条件
        :return: 返回城市和省份的参数字典
        :rtype:dict
        """
        res = {}
        with open('city.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for _ in lines:
            key, value = _.strip().split(":")
            res[key] = value

        province_dic = {}
        city_dic = {}
        for key, value in res.items():
            if '全部' in key:
                province_dic[key] = value
            elif key.split('-')[1] in ['北京市', '上海市', '天津市', '重庆市']:
                province_dic[key] = value
                city_dic[key.split('-')[1]] = value
            else:
                city_dic[key.split('-')[1]] = value
        province_dic.pop('香港特别行政区-全部')
        province_dic.pop('澳门特别行政区-全部')
        return {'province': province_dic, 'city': city_dic}

    def get_area(self):
        """
        从缓存中读取地区的参数条件
        :return: 返回地区的参数字典
        :rtype:dict
        """
        res = {}
        with open('area.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for _ in lines:
            key, value = _.strip().split(":")
            res[key] = value
        # res = redis_conn.rhgetall('area')
        area_dic = {}
        for key, value in res.items():
            area_dic[key] = {
                'base': self.city_dic[key.split('-')[0]],
                'area_code': value}
        return area_dic

    def to_md5(self, sep):
        """
        转MD5
        :param sep: 需要转换的字符串
        :return: 返回转换后的字符串
        """
        m = hashlib.md5(sep.encode(encoding='utf-8'))
        return m.hexdigest()

    def image_handle(self):
        '''
        验证码处理
        :return:
        '''
        self.driver.set_window_size(900, 1000)
        self.driver.get_screenshot_as_file('{}img_normal{}.png'.format(self.img_path,str(self.skip_count)))
        #获取验证码元素的坐标
        captchaElem = self.driver.find_element_by_xpath("//div[@class='new-box94']")
        #获取验证码元素的大小
        left = int(captchaElem.location['x'])
        top = int(captchaElem.location['y'])
        right = int(captchaElem.location['x'] + captchaElem.size['width'])
        bottom = int(captchaElem.location['y'] + captchaElem.size['height'])
        try:
            #打开
            image_info = Image.open('{}img_normal{}.png'.format(self.img_path,str(self.skip_count)))
            im = image_info.crop((left,top,right,bottom))
            #编辑
            draw = ImageDraw.Draw(im)
            ##设置字体
            'MSYH.TTC'
            newfont = ImageFont.truetype('simkai.ttf', 30)
            draw.text((5, 10), '按照下面文字顺序依次点击!!!', (255,0,255), font=newfont)
            del draw
            im.save('{}screenshot_{}{}.png'.format(self.img_path, 'normal_account',str(self.skip_count)))

            #调用验证码接口
            status = self.use_port()
        except Exception as e:
            self.log.error(e)
            self.log.error("验证码图片存储失败")

    def use_port(self):
        '''
        调取打码平台接口
        :return:
        '''
        try:
            # import rk_python3
            get_data = rk_python3.identify('{}screenshot_{}{}.png'.format(self.img_path, 'normal_account',str(self.skip_count)))
            return self.handle_auth(get_data)
        except Exception as e:
            self.log.error(e)
            self.log.error("验证码接口调用失败")

    def error_auth(self):
        '''
        打码出现错误
        :return:
        '''
        try:
            # 调用平台数据，返回告知错误信息
            # {'Result': '81,153.208,168', 'Id': '9b64b696-28a2-49da-8c9e-dcd670154a56'}
            import rk_python3
            get_error_data = rk_python3.error_id(self.error_id)
            self.log.info("错误id返回平台成功：{}".format(get_error_data))
        except Exception as e:
            self.log.error(e)
            self.log.error("错误id返回平台失败")

    def handle_auth(self,get_data):
        '''
        接口返回数据进行处理，进行验证码点击
        :return:
        '''
        try:
            index_data = get_data["Result"]
            self.error_id = get_data["Id"]
            self.log.info("获取到的验证码坐标:{}".format(index_data))
            self.log.info("获取到的验证码id:{}".format(self.error_id))
            # 进行字符串切割
            split_index = index_data.split(".")
            for _ in split_index:
                #再次分割
                split_one_index = _.split(",")
                x_index = split_one_index[0]
                y_index = split_one_index[1]
                #模拟点击验证码
                element = self.driver.find_element_by_xpath("//div[@class='new-box94']")
                ActionChains(self.driver).move_to_element_with_offset(to_element=element, xoffset = x_index, yoffset = y_index).click().perform()
                time.sleep(1)
            #点击提交submitie
            element = self.driver.find_element_by_xpath("//div[@class='my_btn_web']")
            ActionChains(self.driver).move_to_element(element).click().perform()
            # self.driver.find_element_by_xpath("//div[@class='my_btn_web']").click()
            time.sleep(2)
            # 验证是否打码成功
            if '我们只是确认一下你不是机器人，' in self.driver.page_source:
                self.error_auth()
                return False
        except Exception as e:
            self.log.error(e)
            self.log.error("验证码图片点击失败".format('{}screenshot_{}_{}.png'.format(self.img_path, 'normal_account',str(self.skip_count))))
            # 将打码错误信息返回给打码平台
            self.error_auth()
            #记录
            with open("error_auth_image.txt", "a", encoding="utf-8") as f:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(now_time)
                f.write("\n")
                f.write(str('{}screenshot_{}_{}.png'.format(self.img_path, 'normal_account',str(self.skip_count))))
                f.write("\n")
                f.write("\n")
            f.close()
            #再次调用接口
            self.use_port()