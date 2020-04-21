import time
from selenium import webdriver
import pymongo
import os
import logging as log
import datetime
import hashlib
from PIL import Image,ImageFont,ImageDraw
from selenium.webdriver.common.action_chains import ActionChains
chromeOptions = webdriver.ChromeOptions()

class DownNameSpider(object):
    """
    5000-10000/4000-5000公司下载报告方式
    """
    def __init__(self, exc_path, imgpath):
        '''
        数据初始化
        '''
        self.home_url = "https://www.tianyancha.com"
        self.login_url = "https://www.tianyancha.com/login"
        self.humans_url = "https://www.tianyancha.com/humans"
        # =====================
        self.client = pymongo.MongoClient(
            'mongodb://rwuser:48bb67d7996f327b@10.0.0.120:57017,10.0.0.121:57017,10.0.0.122:57017/?replicaSet=rs1')
        self.db = self.client["tyc_com"]
        # 数据库取出账号数据
        self.vip_account_collection = self.db["vip_account_results"]
        # 数据库取出人名数据
        self.name_collection = self.db["name_results"]
        # 数据库取出关键字条件
        self.keyword_collection = self.db['keyword_results']
        # 人名
        self.man_name = None
        # 图片路径
        self.img_path = imgpath
        # 账号
        self.account_num = None
        # 密码
        self.password = None
        # 数据库库取出的一条数据
        self.item = None
        # 数据库一条人名信息
        self.name_item = None
        # 记录账号已经使用几次vip特权
        self.db_use_num = 0
        # =======================
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': exc_path}
        chromeOptions.add_experimental_option('prefs', prefs)
        # 设置代理
        chromeOptions.add_argument("--proxy-server=http://112.117.47.222:9999")
        # path = r'C:\Users\XIII-UP\AppData\Local\Google\Chrome\Application\chromedriver'
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        # --------------------
        # 用于存放所有姓氏
        self.all_name_links = []
        # 用于存放某个姓氏下的所有url
        self.links_page_url = []
        # 用于对姓名打标记传入数据库作为一个字段
        self.last_name_flag = None
        # 用于标记正在抓取姓氏详情的url
        self.link_page_flag = None
        # 用于标记正在抓取姓氏url
        self.link_name_flag = None
        # 用于标记账号列表正在使用的账号坐标
        self.name_list_index = 0
        # 用于某个姓氏抓取到第几页的记录
        self.start_num = None
        # 未清理前的总页码
        self.all_page_str = None
        # 某个姓氏总页码
        self.page_num = None
        # 验证码命名
        self.auth_num = 1
        # 打码错误，返回打码id
        self.error_id = None
        # 用于存放人名
        self.name_list = []
        # 某人所有公司数量
        self.all_company_num = None
        # 某个人需要存储的一条完整数据
        self.save_datas = []
        # 某个人的所有公司url
        self.all_company_urls = []
        # 记录记录到哪条公司的数据，用于对应该公司的url
        self.n = 0
        # 某个名字的列表
        self.man_urls_list = []
        # -------------
        # 要存储的字段
        self.gongsi_mingcheng = None
        # 公司所在省份
        self.gogsi_shengfen = None
        # 开业日期
        self.kaiye_riqi = None
        # 注册资本
        self.zhuce_ziben = None
        # 角色
        self.juese = None
        # 经营状态
        self.jingying_zhuangtai = None
        # 该人的所有公司数量
        self.gongsi_shuliang = None
        # 该公司的详情url
        self.gongsi_xiangqing_url = None
        # ----------------------
        self.label_name = None
        # 某个名字首页
        self.home_name_url = None
        # 导出文件的名字列表页源码
        self.html = None
        # 下载页面刷新后的数据
        self.html_page2 = None
        self.startpart2 = None
        self.endpart2 = None
        # 下载地址
        self.download_url = None
        # 判断是否登陆成功标记位
        self.flag = True
        # 人名获取条件
        self.allow_nums = [[4000, 5000]]
        self.allow_num = [4000, 5000]
        self.allow_page = 1

    # 主程序入口
    def run(self):
        # 登陆
        self.login()
        # 获取人名
        while True:
            self.get_name_to_search()
            self.get_home_url()

    def get_home_url(self):
        '''
        首次登录
        :return:
        '''
        self.driver.get(self.home_url)
        time.sleep(2)
        self.handle_question()

    def get_name_to_search(self):
        '''
        同一个账号，（首次或再次）获取人名进行搜索
        :return:
        '''
        # 从数据库取出一个人名
        # self.search_name_from_mongo()
        self.search_keyword_from_mongo()
        try:
            # 关键字搜索的时候直接访问链接
            self.driver.get(self.man_name)
            # #点击搜索框进行人名输入
            # self.driver.find_element_by_xpath("//input[@id='home-main-search']").send_keys(self.man_name)
            # #点击搜索
            # self.driver.find_element_by_xpath("//div[@class='mt10 js-search-container']//div[@class='input-group-btn btn -hg']").click()
            #这里必须加智能等待，容易报错
            time.sleep(3)
            # 在点击搜索的时候，有的账号会遇到验证码
            self.handle_question()
        except Exception as e:
            log.error("{}".format(e))
            log.info("get_name_to_search异常")
            self.handle_question()
        #  修改名字状态
        # self.db.name_results.update_one({'name': self.man_name}, {'$set': {"flag": 1}})
        # 修改关键字状态
        self.db.keyword_results.update_one({'url': self.man_name}, {'$set': {"flag": 1}})

    def search_name_from_mongo(self):
        '''
        从数据库查询人名
        :return:
        '''
        while True:
            try:
                # 添加新字段
                res = self.name_collection.find_one({"company_numm": {'$gte': self.allow_num[0], '$lte': self.allow_num[1]}, 'flag': 0})
                # log.info(cursor)
                if res:
                    # 人名
                    self.man_name = res["name"]
                    self.last_name = res["last name"]
                    if len(self.man_name) > 10:
                        #切割取值
                        self.handle_long_name()
                        continue
                    else:
                        log.info("[INFO]： 姓名：{}".format(self.man_name))
                        break
                else:
                    if self.allow_nums:
                        self.allow_num = self.allow_nums.pop()
                        if self.allow_num[0] == 5000:
                            self.allow_page = 2
                        else:
                            self.allow_page = 1
                        continue
                    else:
                        log.info("数据库没有符合要求的人名")
                        self.driver.quit()
                        quit()
            except Exception as e:
                log.error("[ERROR]: {}".format(e))
                log.error("[ERROR]: 数据库查询人名失败")

    def search_keyword_from_mongo(self):
        '''
        从数据库查询关键字
        :return:
        '''
        while True:
            try:
                # 添加新字段
                # res = self.keyword_collection.find_one(
                #     {"company_num": {'$gte': self.allow_num[0], '$lte': self.allow_num[1]},'url':{'$regex': 'ola1'}, 'flag': 0})
                res = self.keyword_collection.find_one(
                    {"company_num": {'$gte': self.allow_num[0], '$lte': self.allow_num[1]},
                     'flag': 0})
                # log.info(cursor)
                if res:
                    # 人名
                    self.man_name = res["url"]
                    # self.last_name = res["last name"]
                    # if len(self.man_name) > 10:
                    #     # 切割取值
                    #     self.handle_long_name()
                    #     continue
                    # else:
                    log.info("[INFO]： 查询条件：{}".format(self.man_name))
                    break
                else:
                    if self.allow_nums:
                        self.allow_num = self.allow_nums.pop()
                        if self.allow_num[0] == 5000:
                            self.allow_page = 2
                        else:
                            self.allow_page = 1
                        continue
                    else:
                        log.info("数据库没有符合要求的关键字条件")
                        self.driver.quit()
                        quit()
            except Exception as e:
                log.error("[ERROR]: {}".format(e))
                log.error("[ERROR]: 数据库查询关键字条件失败")

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
                self.name_collection.insert(data)
                log.info("[INFO]: 切割数据，数据存储中...")
                #存储完毕继续进行下一个名字获取
                # self.search_name_from_mongo()
            except Exception as e:
                log.info("[INFO]: 数据已经存在,正在过滤中...")


    def search_accunt_from_mongo(self):
        '''
        从数据库查询账号用于登录
        :return:
        '''
        try:
            res = self.vip_account_collection.find_one({"account_rank": 1,"usable": 0, "flag": 0,"use_num": {"$lt": 10}})
            if res:
                # 账号
                self.account_num = res["account_name"]
                log.info("[INFO]: 正在使用账号{}".format(str(self.account_num)))
                # 密码
                self.password = res["password"]
                #账号使用下载次数
                self.db_use_num = res["use_num"]
            else:
                log.info("数据库没有符合要求的账号")
                self.vip_account_collection.update_many({},{'$set': {'flag': 0, 'use_num': 0}})
                self.driver.quit()
                quit()
        except Exception as e:
            log.error(e)
            log.error("数据库查询账号失败")

    def login(self):
        '''
        登录
        :return:
        '''
        while self.flag:
            try:
                self.driver.get(self.login_url)
                time.sleep(2)
                self.search_accunt_from_mongo()
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
                log.error(e)
                log.error("登录失败")
                self.driver.quit()
                quit()

    def handle_question(self):
        '''
        判断是否登录成功
        :return:
        '''
        # 如果找到首页元素，即登录成功
        try:
            home_pages = self.driver.find_element_by_xpath("//input[@id='home-main-search']")
            time.sleep(3)
            if home_pages:
                self.flag = False
                return
        except Exception as e:
            # 如果找到登录页面元素，即账号不可用，登录失败
            try:
                no_use = self.driver.find_element_by_xpath("//div[@class='pb30 position-rel']/input")
                if no_use:
                    with open("error_account.txt", "a", encoding="utf-8") as f:
                        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        # log.info(now_time)
                        f.write(now_time)
                        f.write("\n")
                        f.write(str(self.account_num))
                        f.write("\n")
                        f.write("\n")
                        log.info("[ERROR]: 手机号或密码错误，失效账号正在记录:{}".format(str(self.account_num)))
                        #标记为不可用，下次不再取出
                        self.vip_account_collection.update_one({'account_name': self.account_num}, {'$set': {"usable" : 1}})
                    f.close()
                    return
            except Exception as e:
                # 如果出现人名列表页(一般是在点击搜索按钮后弹出验证码，验证码解决后）
                try:
                    html1 = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
                    startpart1 = '<span>天眼查为你找到<em class=" f14 in-block vertival-middle pt15 pb15 pr5 pl5">'
                    # 第一种解析
                    if html1.find(startpart1) != -1:
                        start = '</span>个项目品牌/投资机构'
                        # 第一种解析的第1个“导出联系方式”点击
                        if html1.find(start) != -1:
                            # 滑动，看到标签再点击
                            move_button = self.driver.find_element_by_xpath(
                                "//*[@id='web-content']/div/div/div/div[1]/div[5]/div[1]/div[2]/div[2]/div[1]/div[4]/span[1]")
                            self.driver.execute_script("arguments[0].scrollIntoView(false);", move_button)
                            time.sleep(2)
                            self.driver.find_element_by_xpath("//*[@id='search']/div[1]/span").click()
                            time.sleep(3)
                            self.the_user_center()
                         # 第一种解析的第2个“导出联系方式”点击
                        else:
                            time.sleep(2)
                            # 如果不用滑动就直接点击
                            self.driver.find_element_by_xpath("//*[@id='search']/div[1]/span").click()
                            time.sleep(3)
                            self.the_user_center()
                            # self.click_the_button()
                    #第二种解析
                    else:
                        log.info("[INFO]: 第二种列表解析页面")
                        startpart2 ='<span>天眼查为你找到</span><span class="num">&nbsp;'
                        if html1.find(startpart2) != -1:
                            start = '</span>个项目品牌/投资机构'
                            # 第二种解析的第1个“导出联系方式”点击（滑动再点）
                            if html1.find(start) != -1:
                                # 滑动，看到标签再点击
                                try:
                                    move_button =self.driver.find_element_by_xpath("//*[@id='web-content']/div/div[1]/div[3]/div[3]/div[1]/div[3]/span[1]")
                                    self.driver.execute_script("arguments[0].scrollIntoView(false);", move_button)
                                except Exception:
                                    pass
                                # 关键字下载的方式
                                while True:
                                    if self.db_use_num <= 9:
                                        self.driver.find_element_by_xpath("//div[@class='result-tips']/div/a").click()
                                        time.sleep(5)
                                        if 'myorder' in self.driver.current_url:
                                            self.the_user_center()
                                            break
                                        else:
                                            # flag为1，下次不再获取
                                            self.vip_account_collection.update_one(
                                                {'account_name': self.account_num}, {'$set': {"flag": 1}})
                                            # 取新的账号去下载
                                            self.flag = True
                                            self.login()
                                    else:
                                        # flag为1，下次不再获取
                                        self.vip_account_collection.update_one(
                                            {'account_name': self.account_num}, {'$set': {"flag": 1}})
                                        # 取新的账号去下载
                                        self.flag = True
                                        self.login()
                            # 第二种解析的第2个“导出联系方式”点击（直接点）
                            else:
                                log.info("第二种页面的联系人第二种解析")
                                # log.info("注册资本降序")
                                # 点击排序
                                key = self.driver.current_url.split('?')[1]
                                # 点击注册资本降序
                                # 关键字下载的方式
                                while True:
                                    if self.db_use_num <= 9:
                                        self.driver.find_element_by_xpath("//div[@class='result-tips']/div/a").click()
                                        time.sleep(5)
                                        if 'myorder' in self.driver.current_url:
                                            self.the_user_center()
                                            break
                                        else:
                                            # flag为1，下次不再获取
                                            self.vip_account_collection.update_one(
                                                {'account_name': self.account_num}, {'$set': {"flag": 1}})
                                            # 取新的账号去下载
                                            self.flag = True
                                            self.login()
                                    else:
                                        # flag为1，下次不再获取
                                        self.vip_account_collection.update_one(
                                            {'account_name': self.account_num}, {'$set': {"flag": 1}})
                                        # 取新的账号去下载
                                        self.flag = True
                                        self.login()
                                # 名字下载的方式
                                # for _ in range(self.allow_page):
                                #     if _ == 0:
                                #         log.info("注册资本降序")
                                #     else:
                                #         log.info("注册资本升序")
                                #     while True:
                                #         if self.db_use_num <= 9:
                                #             self.driver.get('https://www.tianyancha.com/search/ola{}?{}'.format(_+1, key))
                                #             time.sleep(1)
                                #             self.driver.find_element_by_xpath("//div[@class='result-tips']/div/a").click()
                                #             time.sleep(5)
                                #             if 'myorder' in self.driver.current_url:
                                #                 self.the_user_center()
                                #                 break
                                #             else:
                                #                 # flag为1，下次不再获取
                                #                 self.vip_account_collection.update_one(
                                #                     {'account_name': self.account_num}, {'$set': {"flag": 1}})
                                #                 # 取新的账号去下载
                                #                 self.flag = True
                                #                 self.login()
                                #         else:
                                #             # flag为1，下次不再获取
                                #             self.vip_account_collection.update_one(
                                #                 {'account_name' : self.account_num}, {'$set': {"flag": 1}})
                                #             # 取新的账号去下载
                                #             self.flag = True
                                #             self.login()
                except Exception as e:
                    # 如果出现验证码
                    try:
                        self.driver.find_element_by_xpath("//div[@class='container']//div[@class='content']")
                        self.image_handle()
                    # 如果出现检索条件过大，或者账号暂时不可用
                    except Exception as e:
                        try:
                            html = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
                            startpart = '<div class="f24 mb40 mt40 sec-c1 ">'
                            endpart = '</div>'
                            end = 0
                            while html.find(startpart, end) != -1:
                                start = html.find(startpart, end) + len(startpart)
                                end = html.find(endpart, start)
                                error_str = html[int(start):int(end)]
                                if error_str == "抱歉，没有找到相关结果！":
                                    log.info("[ERROR]: 抱歉，没有找到相关结果！")
                                    with open('to_big_name.txt', 'a') as f:
                                        f.write('{}\n'.format(self.man_name))
                                    # 继续搜索下一个名字
                                    # self.get_name_to_search()
                        except Exception as e:
                            # 匹配错误提示信息
                            # 不建议写在try中，因为都能匹配到
                            error_info = self.driver.find_element_by_xpath("/html/body/div/div[1]").text
                            if error_info == "系统检测到您非人类行为，己被禁止访问天眼查，若有疑问请联系官方qq群 515982002":
                                log.info("[ERROR]: {}".format(error_info))
                                self.vip_account_collection.update_one({'account_name': self.account_num}, {'$set': {"flag": 1}})
                                self.flag = True
                                self.login()

    def the_user_center(self):
        '''
        用户中心,进入该函数说明次数没用完
        :return:
        '''
        while True:
            self.html_page2 = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
            # log.info(html)
            self.startpart2 = '<span class="reportstatus1 ">'
            self.endpart2 = '</span>'
            end2 = 0
            # 找到说明界面跳转到了个人中心
            if self.html_page2.find(self.startpart2, end2) != -1:
                log.info("跳转下载页面成功：该账号{}下载次数已达次数【{}】".format(str(self.account_num), int(self.db_use_num) + 1))
                start = self.html_page2.find(self.startpart2, end2) + len(self.startpart2)
                end = self.html_page2.find(self.endpart2, start)
                wei_button = self.html_page2[int(start):int(end)]
                # 找到“未生成”标签（第一行）
                if wei_button == "未生成":
                    log.info("未生成,等待中...")
                    self.refresh_page()
                elif wei_button == "生成中":
                    log.info("生成中,等待中...")
                    self.refresh_page()
            else:
                break
        #找不到未生成"或者"生成中"提示，说明能够下载
        self.download_page()

    def refresh_page(self):
        '''
        点击刷新界面
        :return:
        '''
        #点击刷新
        time.sleep(5)
        self.driver.refresh()
        #再判断是否还存在“未生成”标签
        self.html_page2 = None
        self.startpart2 = None
        self.endpart2 = None
        # self.the_user_center()

    def download_page(self):
        '''
        点击下载按钮
        :return:
        '''
        try:
            html_page3 = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
            # log.info(html)
            startpart3 = '<a target="_blank" href="'
            endpart3 = '" class="tblue point pr20 ">下载</a>'
            end3 = 0
            if html_page3.find(startpart3, end3) != -1:
                start = html_page3.find(startpart3, end3) + len(startpart3)
                end = html_page3.find(endpart3, start)
                self.download_url = html_page3[int(start):int(end)]
                # 找到“未生成”标签（第一行）
                if self.download_url:
                    log.info("生成成功，等待下载中...")
                    self.driver.get(self.download_url)
                    self.db_use_num += 1
                    # 修改会员使用下载状态
                    self.vip_account_collection.update_one({'account_name': int(self.account_num)},{'$set': {"use_num": self.db_use_num}})
                    time.sleep(2)
            #找不到说明未生成，再次刷新
            # self.refresh_page()
        except Exception as e:
            log.error(e)
            log.error("xiazai异常")
            # # 再判断是否还存在“未生成”标签
            # self.html_page2 = None
            # self.startpart2 = None
            # self.endpart2 = None
            # self.the_user_center()

    def image_handle(self):
        '''
        验证码处理
        :return:
        '''
        self.driver.get_screenshot_as_file('{}img_down_spider.png'.format(self.img_path))
        #获取验证码元素的坐标
        captchaElem = self.driver.find_element_by_xpath("//div[@class='new-box94']")
        #获取验证码元素的大小
        left = int(captchaElem.location['x'])
        top = int(captchaElem.location['y'])
        right = int(captchaElem.location['x'] + captchaElem.size['width'])
        bottom = int(captchaElem.location['y'] + captchaElem.size['height'])
        try:
            #打开
            image_info = Image.open('{}img_down_spider.png'.format(self.img_path))
            im = image_info.crop((left,top,right,bottom))
            #编辑
            draw = ImageDraw.Draw(im)
            ##设置字体
            newfont = ImageFont.truetype('simkai.ttf', 30)
            draw.text((5, 10), '按照下面文字顺序依次点击!!!', (255,0,255), font=newfont)
            del draw
            im_name = im.save('{}screenshot_{}.png'.format(self.img_path, 'down_name'))
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
            get_data = rk_python3.identify('{}screenshot_{}.png'.format(self.img_path, 'down_name'))
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
            log.info("验证码图片点击失败".format('screenshot_{}.png'.format('down_name')))
            # 将打码错误信息返回给打码平台
            self.error_auth()
            #记录
            with open("error_auth_image.txt", "a", encoding="utf-8") as f:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(now_time)
                f.write("\n")
                f.write(str('screenshot_{}.png'.format('down_name')))
                f.write("\n")
                f.write("\n")
            f.close()
            #再次调用接口
            self.use_port()

if __name__=='__main__':
    realpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/log/"
    imgpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/img/"
    excpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/exc/"
    filename = "{}down_name_report_debug_{}.log".format(realpath, time.strftime("%Y-%m-%d", time.localtime()))

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

    base = DownNameSpider(excpath , imgpath)
    base.run()