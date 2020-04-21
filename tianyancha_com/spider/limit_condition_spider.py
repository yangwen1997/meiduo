import time
import os
import logging as log
import pymongo
import datetime
import math
import re
import json
import urllib.parse
import hashlib
from selenium import webdriver
from PIL import Image,ImageFont,ImageDraw
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as B
import sys
sys.path.append(r"E:\projects\04_Coding\spider")
import core as C
chromeOptions = webdriver.ChromeOptions()


class LimitConditionSpider(object):
    """
    >10000的公司添加限定条件
    """
    def __init__(self, img_path):
        """
        数据初始化
        """
        self.login_url = "https://www.tianyancha.com/login"
        # =====================
        # 数据库
        self.client = pymongo.MongoClient(
            'mongodb://rwuser:48bb67d7996f327b@10.0.0.120:57017,10.0.0.121:57017,10.0.0.122:57017/?replicaSet=rs1')
        # 天眼查查询数据库
        self.db = self.client["tyc_com"]
        self.account_collection = self.db["account_results"]
        self.name_results = self.db["name_results"]
        # 数据存储目标数据库
        self.all_com_db = self.client["all_com"]
        self.all_com_collection = self.all_com_db["new_results"]
        self.img_path = img_path
        # 一条账号数据
        self.accunt_item = None
        # 账号
        self.account_num = None
        # 密码
        self.password = None
        # 一条名字数据
        self.name_item = None
        # 人名
        self.man_name = None
        # 姓氏
        self.last_name = None
        # =======================
        # 设置代理
        chromeOptions.add_argument("--proxy-server=http://10.0.0.50:9999")
        path = r'C:\Users\XIII-UP\AppData\Local\Google\Chrome\Application\chromedriver'
        self.driver = webdriver.Chrome(chrome_options=chromeOptions, executable_path=path)
        # --------------------
        # 验证码命名
        self.auth_num = 1
        # 打码错误，返回打码id
        self.error_id = None
        # -------------
        self.label_name = None
        # 某个名字首页
        self.home_name_url = None
        # 名字数量
        self.name_num = None
        # 公司数量
        self.company_num = None
        # -------------
        # 数据存储
        self.companyName = None
        self.companyUrl = None
        self.businessState = None
        self.registerAddress = None
        self.legalMan = None
        self.registerMoney = None
        self.registerTime = None
        self.companyTel = None
        self.companyEmail = None
        self.flag = True
        self.total = 0


    def run(self):
        """
        主程序入口
        :return:
        """
        # 登陆
        self.login()
        # 获取人名
        while True:
            self.limit_condition_search()
            # self.get_home_url()

    def search_account_from_mongo(self):
        '''
        从数据库查询账号用于登录
        :return:
        '''
        try:
            cursor = self.db.account_results.find({"account_rank": 0, "usable": 0, "flag": 0}).limit(1)
            # log.info(cursor)
            if cursor:
                for self.accunt_item in cursor:
                    # 账号
                    self.account_num = self.accunt_item["account_name"]
                    log.info("[INFO]: 正在使用账号{}".format(self.account_num))
                    # 密码
                    self.password = self.accunt_item["password"]
            else:
                log.info("数据库没有符合要求的账号")
                self.driver.quit()
                quit()
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("[ERROR]: 数据库查询账号失败")

    def limit_condition_search(self):
        """
        条件限定处理
        :return:
        """
        # 从数据库取出一个人名
        self.search_name_from_mongo()
        log.info("[INFO]: 正在获取人名详情：{}".format(self.man_name))
        log.info('公司总数：{}'.format(self.total))
        lists = []
        first_conditions = ['or0100', 'or100200', 'or200500', 'or5001000', 'or1000']
        now_num = 0
        for _ in range(len(first_conditions)):
            first_num = self.get_name_to_search(first_conditions[_])
            if first_num is None:
                log.error('获取公司数目失败')
                break
            now_num += int(first_num)
            log.info('条件[{}]下当前公司数量：{}'.format(first_conditions[_], first_num))
            surplus_num = self.total - now_num
            log.info('剩余公司数量：{}'.format(surplus_num))
            if int(first_num) > 10000:
                """第二种条件"""
                second_lists = self.second_limit_condition(int(first_num), first_conditions[_])
                if second_lists:
                    lists.extend(second_lists)
                else:
                    log.error('第二种条件失败')
            else:
                lists.append({'total': int(first_num),'url': self.name_url})
            if surplus_num < 10000:
                if _ <=2:
                    condition = first_conditions[_][-3:]
                else:
                    condition = first_conditions[_][-4:]
                self.name_url = "https://www.tianyancha.com/search/or{}5000?key={}".format(condition, self.label_name)
                lists.append({'total': int(surplus_num), 'url': self.name_url})
                break
            else:
                continue
        print({'name': self.man_name, 'data': lists})
        # data = json.dumps({lists}, ensure_ascii=False)
        if lists:
            # 数据写进缓存
            re_db = C.redis_db()
            re_db.rset(self.man_name, json.dumps({lists}, ensure_ascii=False))
            #  修改名字状态
            self.db.name_results.update_one({'name': self.man_name}, {'$set': {"flag": 1}})

    def second_limit_condition(self, total, first_condition):
        second_lists = []
        second_conditions = ['e01', 'e015', 'e510', 'e1015', 'e15']
        now_num = 0
        for _ in range(len(second_conditions)):
            condition = '{}-{}'.format(first_condition, second_conditions[_])
            second_num = self.get_name_to_search(condition)
            if second_num is None:
                log.error('获取第二条件公司数目失败')
                break
            now_num += int(second_num)
            log.info('条件[{}]下当前公司数量：{}'.format(condition, second_num))
            surplus_num = total - now_num
            log.info('剩余公司数量：{}'.format(surplus_num))
            if int(second_num) > 10000:
                log.info('需要添加第三种条件')
                second_lists.append({'total': int(second_num), 'url': self.name_url})
            else:
                second_lists.append({'total': int(second_num), 'url': self.name_url})
            if surplus_num <= 0:
                break
            else:
                continue
        return second_lists

    def get_name_to_search(self, condition):
        '''
        进行url拼接，访问
        :return:
        '''
        # 从数据库取出一个人名
        # self.search_name_from_mongo()
        # 进行编码转换
        self.label_name = urllib.parse.quote(self.man_name)
        # 例如"https://www.tianyancha.com/search?key=%E5%BC%A0%E4%BC%9F"
        self.name_url ="https://www.tianyancha.com/search/{}?key={}".format(condition, self.label_name)
        try:
            self.driver.get(self.name_url)
            # log.info("[INFO]: 正在获取人名详情：{}".format(self.man_name))
            log.info(self.name_url)
            time.sleep(3)
            # 跳转页面有时会遇到验证码
            return self.handle_question()
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("[ERROR]: get_name_list异常")
            # 初次登录遇到验证码
            self.handle_question()

    def search_name_from_mongo(self):
        '''
        从数据库查询人名
        :return:
        '''
        while True:
            try:
                #添加新字段
                cursor = self.db.name_results.find({"company_numm": {'$gte': 10000}, 'flag': 0}).limit(1)
                # log.info(cursor)
                if cursor:
                    for self.name_item in cursor:
                        # 人名
                        self.man_name = self.name_item["name"]
                        self.last_name = self.name_item["last name"]
                        self.total = self.name_item['company_numm']
                    if len(self.man_name) > 10:
                        #切割取值
                        self.handle_long_name()
                        continue
                    else:
                        break
                        log.info("[INFO]： 姓名：{}".format(self.man_name))
                else:
                    log.info("数据库没有符合要求的人名")
                    self.driver.quit()
                    quit()
            except Exception as e:
                log.info("[ERROR]: {}".format(e))
                log.info("[ERROR]: 数据库查询人名失败")

    def handle_long_name(self):
        '''
        切割长度过长的名字
        :return:
        '''
        #以姓氏作为节点切割
        name_split_list = self.man_name.split(self.last_name)
        log.info("[INFO]: 切割后的名字列表：{}".format(name_split_list))
        for info in name_split_list:
            log.info("[INFO]: 切割后的名字：{}".format(info))
            m = hashlib.md5(info.encode(encoding='utf-8'))
            change_name = m.hexdigest()
            try:
                data = {
                    "_id": change_name,
                    "name": info,
                    "last name": self.last_name,
                    "flag": 0,
                }
                log.info(data)
                self.name_results.insert(data)
                log.info("[INFO]: 切割数据，数据存储中...")
                #存储完毕继续进行下一个名字获取
                # self.search_name_from_mongo()
            except Exception as e:
                log.info("[INFO]: 数据已经存在,正在过滤中...")

    def login(self):
        '''
        登录
        :return:
        '''
        while self.flag:
            try:
                self.driver.get(self.login_url)
                time.sleep(2)
                self.search_account_from_mongo()
                # 账号
                self.driver.find_element_by_xpath("//div[@class='pb30 position-rel']/input").send_keys(self.account_num)
                # 密码
                self.driver.find_element_by_xpath("//div[@class='pb40 position-rel']/input").send_keys(self.password)
                # 点击登录，成功直接跳转首页
                self.driver.find_element_by_xpath(
                    "//div[@class='module module1 module2 loginmodule collapse in']/div/div[5]").click()
                # 这里必须加上时间等待，不然又再匹配登录页面
                time.sleep(2)
                self.handle_question()
            except Exception as e:
                log.info("[ERROR]: {}".format(e))
                log.info("[ERROR]: 登录失败")

    def handle_question(self):
        '''
        判断是否登录成功
        :return:
        '''
        try:
            #如果跳转到首页即登录成功
            home_pages = self.driver.find_element_by_xpath("//input[@id='home-main-search']")
            if home_pages:
                #提前打标记
                self.db.account_results.update_one({'_id': self.accunt_item['_id']}, {'$set': {"flag": 1}})
                self.flag=False
                return
        except Exception as e:
            # 如果找到登录页面元素，即账号不可用，登录失败
            try:
                no_use = self.driver.find_element_by_xpath("//div[@class='pb30 position-rel']/input")
                if no_use:
                    # 提前打标记
                    # 标记为不可用，下次不再取出
                    self.db.account_results.update_one({'account_name': self.account_num}, {'$set': {"usable": 1}})
                    return
            except Exception as e:
                # 获取列表页所有详情urls
                # 公司数量
                html0 = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
                startpart0 = '<span>天眼查为你找到</span><span class="num">&nbsp;'
                end0 = 0
                # 老板数量
                startpart00 = '天眼查为你找到<span class="num-company-distributed">&nbsp;'
                end00 = 0
                if html0.find(startpart0, end0) != -1:

                    return self.parse_company_pages()
                    # # 存储
                    # self.update_name_db()
                    # 获取新的名字进行访问
                    # self.get_name_to_search()
                elif html0.find(startpart0, end0) != -1 or html0.find(startpart00, end00) != -1:
                    log.info("[ERROR]: 找不到公司数量或者人名数量！")
                    with open('error_limit_search.txt', 'a') as f:
                        f.write('name: {}'.format(self.man_name))
                        f.write('url: {}'.format(self.name_url))
                        f.write('ERROR: 找不到公司数量或者人名数量\n\n')
                    # 更新名字数量
                    # self.db.name_results.update_one({'_id': self.name_item['_id']},{'$set': {"name_num": 0}})
                    # # 更新公司数量
                    # self.db.name_results.update_one({'_id': self.name_item['_id']},{'$set': {"company_numm": 0}})
                    # self.get_name_to_search()
                #都找不到说明没有进入列表页
                else:
                    try:
                        self.driver.find_element_by_xpath("//div[@class='container']//div[@class='content']")
                        self.image_handle()
                    # 如果出现检索条件过大，或者账号暂时不可用
                    except Exception as e:
                        if '普通用户可查看100家公司，VIP会员可查看5000家公司' in self.driver.page_source:
                            # 提前打标记
                            self.db.account_results.update_one({'_id': self.accunt_item['_id']}, {'$set': {"flag": 1}})
                            # self.search_name_from_mongo()
                            # self.get_name_to_search()
                        else:
                            try:
                                error_str = self.driver.find_element_by_xpath("//div[@class='f24 mb40 mt40 sec-c1 ']").text
                                if error_str == "抱歉，没有找到相关结果！":
                                    log.info("[ERROR]: 抱歉，没有找到相关结果！")
                                    with open('error_limit_search.txt', 'a') as f:
                                        f.write('name: {}'.format(self.man_name))
                                        f.write('url: {}'.format(self.name_url))
                                        f.write('ERROR: 抱歉，没有找到相关结果\n\n')
                                    # 继续搜索下一个名字
                                    # 更新名字数量
                                    # self.db.name_results.update_one({'_id': self.name_item['_id']},{'$set': {"name_num": 0}})
                                    # 更新公司数量
                                    # self.db.name_results.update_one({'_id': self.name_item['_id']},{'$set': {"company_numm": 0}})
                                    # self.get_name_to_search()
                            except Exception as e:
                                # 匹配错误提示信息
                                error_info = self.driver.find_element_by_xpath("/html/body/div/div[1]").text
                                if error_info == "系统检测到您非人类行为，己被禁止访问天眼查，若有疑问请联系官方qq群 515982002":
                                    log.info("[ERROR]: {}".format(error_info))
                                    self.db.account_results.update_one({'_id': self.accunt_item['_id']}, {'$set': {"flag": 1}})
                                    self.flag = True
                                    self.login()

    def parse_company_pages(self):
        '''
        判断该名字的数量是否在范围内
        :return:
        '''
        while True:
            try:
                # 获取列表页所有详情urls
                list_html = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
                # startpart2 = '天眼查为你找到<span class="num-company-distributed">&nbsp;'
                # endpart2 = '&nbsp;</span>位同名老板'
                # end2 = 0
                # if list_html.find(startpart2, end2) != -1:
                #     start = list_html.find(startpart2, end2) + len(startpart2)
                #     end = list_html.find(endpart2, start)
                #     name_num_str = list_html[int(start):int(end)]
                #     self.name_num = int(name_num_str)
                    # log.info("[INFO]: 该名字老板数量:{}".format(self.name_num))
                #===================================
                startpart3 = '<span>天眼查为你找到</span><span class="num">&nbsp;'
                endpart3 = '&nbsp;</span>家公司'
                end3 = 0
                if list_html.find(startpart3, end3) != -1:
                    start = list_html.find(startpart3, end3) + len(startpart3)
                    end = list_html.find(endpart3, start)
                    company_num_str = list_html[int(start):int(end)]
                    self.company_num = int(company_num_str)
                    # log.info("[INFO]: 该名字公司数量:{}".format(self.company_num))
                    return company_num_str
                    #存储更新数据库字段
                    # self.update_name_db()
                    # #判断类型
                    # self.judge_num( self.company_num)
                else:
                    log.info("[ERROR]: 找不到公司数量！")
                    with open('error_limit_search.txt', 'a') as f:
                        f.write('name: {}'.format(self.man_name))
                        f.write('url: {}'.format(self.name_url))
                        f.write('ERROR: 找不到公司数量\n\n')
                        return
                    # self.db.name_results.update_one({'_id': self.name_item['_id']}, {'$set': {"name_num": 0}})
                    # # 更新公司数量
                    # self.db.name_results.update_one({'_id': self.name_item['_id']}, {'$set': {"company_numm": 0}})
                break
                #获取新的名字进行访问
                # self.get_name_to_search()
            except Exception as e:
                log.info("[ERROR]: {}".format(e))
                log.info("parse_company_pages异常")
                break

    def update_name_db(self):
        '''
        修改name_results字段
        :return:
        '''
        try:
            # 更新名字数量
            self.db.name_results.update_one({'_id': self.name_item['_id']}, {'$set': {"name_num": self.name_num}})
            # 更新公司数量
            self.db.name_results.update_one({'_id': self.name_item['_id']}, {'$set': {"company_numm":self.company_num}})
            log.info("[INFO]: 数据更新中...")
        except Exception as e:
            log.info("[INFO]: 数据无法更新...")

    def judge_num(self,no_sure_num):
        '''
        判断公司数量
        :return:
        '''
        # 普通账号只能爬小于100家的
        if no_sure_num <= 100:
            self.get_next_page()

    def get_next_page(self):
        '''
        翻页功能，获取列表页下一页
        :return:
        '''
        #计算总页数( 向上取整)
        company_page = math.ceil(self.company_num / 20)
        log.info("[INFO]: 总页数：{}".format(company_page))
        #拼接url
        for next_link in range(1,int(company_page)+1):
            log.info("[INFO]: 当前页码：{}".format(next_link))
            if next_link != 1:
                next_page_url = "https://www.tianyancha.com/search/p{}?key={}".format(next_link,self.label_name)
                self.driver.get(next_page_url)
                time.sleep(2)
            #解析页面
            self.parse_and_get_list_company()

    def parse_and_get_list_company(self):
        '''
        获取列表页的公司数据
        :return:
        '''
        """另一种策略,不具体定位class里面的值，因为class里面的值会变，所以定位到标签，再用正则做匹配"""
        try:
            # 获取页面html
            html = B(self.driver.page_source, 'html.parser')
            # 找到所有的公司外层的模块
            div_lists = html.find_all('div', attrs={'data-id': re.compile('\d+')})
        except Exception as e:
            log.info('[error]: 找不到所有的公司外层的模块{}'.format(e))
            self.db.account_results.update_one({'_id': self.accunt_item['_id']}, {'$set': {"flag": 0}})
            self.driver.quit()
            quit()

        for div in div_lists:
            dic={}
            try:
                tmp = div.find('a', attrs={'href': re.compile('https://www.tianyancha.com/company/\d+')})
                # 公司名称
                dic['companyName'] = tmp.get_text(strip=True)
                # 公司url
                dic['companyUrl'] = tmp.attrs['href']
                # 经营状态
                dic['businessState'] = tmp.next_sibling.get_text(strip=True)
                # 公司所属省份
                dic['companyProvince'] = div.contents[2].get_text(strip=True)
            except Exception as e:
                log.info('[error]: {}'.format(e))
                quit()
                # log.info('[error]: {}'.format(e))
            # 法人/注册资本/注册时间/联系电话/邮箱/法人信息
            tags = div.contents[1].contents[1:-2]

            data = []
            for tag in tags:
                for _ in tag.contents:
                    data.append(_.get_text(strip=True))
            # 对初步解析的文本进一步分割
            tmp_dic= {'法定代表人':'legalMan',
                      '代表人': 'representMan',
                      '负责人':'chargeMan',
                      '注册资本':'registerMoney',
                      '注册时间':'registerTime',
                      '联系电话':'companyTel',
                      '邮箱':'companyEmail',
                      }
            for _ in data:
                key, value = _.split("：")
                # 联系电话可能存在多个
                if key in ['法定代表人', '代表人', '负责人']:
                    # 法定代表人url
                    try:
                        dic['manUrl'] = div.find('a', attrs={'title': value}).attrs['href']
                    except Exception as e:
                        log.info('[error]: 获取法人链接失败{}'.format(e))
                if key in ['联系电话','邮箱']:
                    try:
                        tel_lists = re.search('.*\[(.*)\].*', value.replace('\"', '')).group(1).split(',')
                    except Exception:
                        tel_lists = [value]
                    dic[tmp_dic[key]] = tel_lists
                else:
                    dic[tmp_dic[key]] = value
            # 数据存储
            self.save_data(dic)
        """---------"""

    def save_data(self, dic):
        '''
        名录数据存储
        :return:
        '''
        try:
            import time
            collect_time = int(time.time() * 1000)      # 入库时间
            m = hashlib.md5(dic.get('companyName').encode(encoding='utf-8'))
            change_name = m.hexdigest()
            companyName = dic['companyName']
            companyUrl = dic['companyUrl']
            del dic['companyName']
            del dic['companyUrl']
            data = {
                "_id": change_name,
                "webSource": "https://www.tianyancha.com/",
                "companyName": companyName,
                "companyUrl": companyUrl,
                "docs":{
                    "background":{
                        "baseInfo": dic
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
                'reportFlag': 0
            }
            # log.info(dic)
            # data['docs']['background']['baseInfo'] = dic
            # log.info(data)
            self.all_com_collection.insert(data)
            log.info("[INFO]: 数据存储中...")
        except Exception as e:
            log.info("[ERROR]: 详细：{}".format(e))
            log.info("[INFO]: 数据已经存在,正在过滤中...")


    def image_handle(self):
        '''
        验证码处理
        :return:
        '''
        self.driver.get_screenshot_as_file('{}img_limit.png'.format(self.img_path))
        #获取验证码元素的坐标
        captchaElem = self.driver.find_element_by_xpath("//div[@class='new-box94']")
        #获取验证码元素的大小
        left = int(captchaElem.location['x'])
        top = int(captchaElem.location['y'])
        right = int(captchaElem.location['x'] + captchaElem.size['width'])
        bottom = int(captchaElem.location['y'] + captchaElem.size['height'])
        try:
            #打开
            image_info = Image.open('{}img_limit.png'.format(self.img_path))
            im = image_info.crop((left,top,right,bottom))
            #编辑
            draw = ImageDraw.Draw(im)
            ##设置字体
            newfont = ImageFont.truetype('simkai.ttf', 30)
            draw.text((5, 10), '按照下面文字顺序依次点击!!!', (255,0,255), font=newfont)
            del draw
            im.save('{}screenshot_{}.png'.format(self.img_path, 'limit_condition'))
            #调用验证码接口
            self.use_port()
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("[INFO]: 验证码图片存储失败")

    def use_port(self):
        '''
        调取打码平台接口
        :return:
        '''
        try:
            import rk_python3
            get_data = rk_python3.identify('{}screenshot_{}.png'.format(self.img_path, 'limit_condition'))
            self.handle_auth(get_data)
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("验证码接口调用失败")

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
            log.info("[ERROR]: 错误id返回平台成功：{}".format(get_error_data))
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("错误id返回平台失败")

    def handle_auth(self,get_data):
        '''
        接口返回数据进行处理，进行验证码点击
        :return:
        '''
        try:
            # #下次图片命名以2、3、4.。。。
            self.auth_num += 1
            index_data = get_data["Result"]
            self.error_id = get_data["Id"]
            log.info("[INFO]: 获取到的验证码坐标:{}".format(index_data))
            log.info("[INFO]: 获取到的验证码id:{}".format(self.error_id))
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
            #点击提交
            self.driver.find_element_by_xpath("//div[@class='my_btn_web']").click()
            time.sleep(2)
            #成功之后会跳转回humans页面
            self.handle_question()
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("验证码图片点击失败".format('{}screenshot_{}.png'.format(self.img_path, 'limit_condition')))
            # 将打码错误信息返回给打码平台
            self.error_auth()
            #记录
            with open("error_auth_image.txt", "a", encoding="utf-8") as f:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(now_time)
                f.write("\n")
                f.write(str('{}screenshot_{}.png'.format(self.img_path, 'limit_condition')))
                f.write("\n")
                f.write("\n")
            f.close()
            #再次调用接口
            self.use_port()


if __name__=='__main__':
    realpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/log/"
    imgpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/img/"
    excpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/exc/"
    filename = "{}limit_condition_debug_{}.log".format(realpath, time.strftime("%Y-%m-%d", time.localtime()))

    log.basicConfig(
        level=log.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y %H:%M:%S',
        filename=filename,
        filemode='w'
    )
    console = log.StreamHandler()
    console.setLevel(log.INFO)
    formatter = log.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    log.getLogger('').addHandler(console)

    normal = LimitConditionSpider(imgpath)
    normal.run()