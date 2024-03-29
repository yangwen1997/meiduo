import datetime, math, re, json, hashlib, urllib.parse, time
import rk_python3
# from gevent import sleep
from time import sleep
from clear_chrome_cache import Clear
from selenium import webdriver
from PIL import Image,ImageFont, ImageDraw
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as B
from common import redis_conn, name_results_coll, account_results_coll,insert_db
chromeOptions = webdriver.ChromeOptions()


class KeywordLimitConditionSpider(object):
    """
    限定条件爬取名录方式
    """
    def __init__(self, img_path, ip, skip_count, proxy_tag):
        """
        数据初始化
        """
        self.total = 0
        self.login_url = "https://www.tianyancha.com/login"
        # =====================
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

        chromeOptions.add_argument("--incognito")
        chromeOptions.add_argument('--disable-extensions')
        chromeOptions.add_argument('--disable-infobars')
        chromeOptions.add_argument('--profile-directory=Default')
        chromeOptions.add_argument('--disable-plugins-discovery')
        if proxy_tag == 1:
            # chromeOptions.add_argument("--proxy-server=http://127.0.0.1")
            # chromeOptions.add_argument("--proxy-server=http://{}".format(ip))
            self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        else:
            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            desired_capabilities['proxy'] = {
                "httpsProxy": ip,
                # "ftpProxy": PROXY,
                # "sslProxy": PROXY,
                "noProxy": None,
                "proxyType": "DIRECT",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
            self.driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=desired_capabilities)
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
        self.flag = True
        self.skip_count = skip_count
        self._id = None
        self.account_id = None
        self.count = 1
        self.check_count = 0
        # 城市keys
        self.city_keys = redis_conn.rhkeys('city')
        # 省份列表
        self.province = self.get_province()
        # 区域keys
        self.area_keys = redis_conn.rhkeys('area')


    def run(self,log):
        """
        主程序入口
        :return:
        """
        try:
            # 登陆
            self.login(log)
            # 获取人名
            while True:
                self.get_name_to_search(log)
        except Exception as e:
            print(e)
            # self.get_home_url()

    def search_account_from_mongo(self, log):
        '''
        从数据库查询账号用于登录
        :return:
        '''
        num = 10
        while num:
            try:
                # try:
                #     account_info = json.loads(redis_conn.rpop('tyc_account_lists').decode())
                # except Exception as e:
                #     print(e)
                #     account_info = None
                account_info = {
                    '_id': '1',
                    'account_name': '15844501142',
                    'password': 'a123456789',
                }
                if account_info:
                    self.account_id = account_info['_id']
                    # self.account_id = account_info['_id']
                    # 账号
                    self.account_num = account_info['account_name']
                    # self.account_num = 15144581447
                    log.info("[INFO]: 正在使用账号{}".format(self.account_num))
                    # 密码
                    self.password = account_info["password"]
                    break
                else:
                    num -= 1
                    sleep(1)
                    continue
            except Exception as e:
                log.info("[ERROR]: {}".format(e))
                log.info("[ERROR]: 数据库查询账号失败")
        if num == 0:
            log.info("数据库没有符合要求的账号")
            self.driver.quit()
            quit()

    def get_name_to_search(self, log):
        '''
        进行url拼接，访问
        :return:
        '''
        # 从数据库取出一个人名
        self.search_name_from_mongo(log)
        # 进行编码转换
        self.label_name = urllib.parse.quote(self.man_name)
        # 例如"https://www.tianyancha.com/search?key=%E5%BC%A0%E4%BC%9F"
        name_url ="https://www.tianyancha.com/search?key="+ self.label_name
        try:
            self.driver.set_window_size(400, 600)
            self.driver.get(name_url)
            self.count += 1
            log.info("正在获取人名详情：{}".format(self.man_name))
            log.info(name_url)
            sleep(3)
            # 跳转页面有时会遇到验证码
            self.handle_question(log)
            print("-----------------\n")
        except Exception as e:
            log.error(e)
            log.info("get_name_list异常")
            # 初次登录遇到验证码
            self.handle_question(log)

    def search_name_from_mongo(self, log):
        '''
        从数据库查询人名
        :return:
        '''
        # skip_count = self.skip_count
        while True:
            try:
                #添加新字段
                # try:
                #     name_info = json.loads(redis_conn.rpop('tyc_name_lists').decode())
                #     res = name_results_coll.find_one({'_id': name_info['_id']})
                #     if res.get('name_num'):
                #         print('已爬取')
                #         continue
                # except Exception as e:
                #     print(e)
                #     name_info = None
                name_info = {
                    '_id': '1',
                    'name': '赵强',
                    'last name': '赵',
                }
                if name_info:
                    # _id
                    self._id = name_info["_id"]
                    # 人名
                    self.man_name = name_info["name"]
                    self.last_name = name_info["last name"]
                    if len(self.man_name) > 10:
                        #切割取值
                        self.handle_long_name(log)
                        continue
                    else:
                        log.info("姓名：{}".format(self.man_name))
                        break
                else:
                    one = name_results_coll.find_one({"name_num": {'$exists': False}})
                    if one:
                        sleep(60)
                        log.info('缓存中暂时没有数据,60s后重试...')
                        continue
                    else:
                        log.info("数据库没有符合要求的人名")
                        self.driver.quit()
                        quit()
            except Exception as e:
                log.error(e)
                log.error("数据库查询人名失败")
                time.sleep(5)

    def handle_long_name(self, log):
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
                name_results_coll.insert(data)
                log.info("[INFO]: 切割数据，数据存储中...")
            except Exception as e:
                log.info("[INFO]: 数据已经存在,正在过滤中...")

    def login(self, log):
        '''
        登录
        :return:
        '''
        while self.flag:
            try:
                self.driver.set_window_size(900, 1000)
                self.driver.get(self.login_url)
                sleep(2)
                self.search_account_from_mongo(log)
                # 点击密码登陆
                self.driver.find_element_by_xpath("//div[@onclick='changeCurrent(1);']").click()
                # 账号
                str = """document.querySelector(".mobile_box .contactphone").value = '{}';document.querySelector(".mobile_box .contactword").value = '{}';""".format(self.account_num, self.password)
                self.driver.execute_script(str)
                # 点击登录，成功直接跳转首页
                self.driver.find_element_by_xpath(
                    "//div[@class='module module1 module2 loginmodule collapse in']/div/div[5]").click()
                # 这里必须加上时间等待，不然又再匹配登录页面
                sleep(3)
                self.handle_question(log)
            except Exception as e:
                log.info("[ERROR]: {}".format(e))
                log.info("[ERROR]: 登录失败")
                sleep(5)

    def handle_question(self, log):
        '''
        判断是否登录成功
        :return:
        '''
        try:
            if ('proxy' or '503' or '500') in self.driver.page_source:
                self.driver.refresh()
                sleep(3)
            #如果跳转到首页即登录成功
            home_pages = self.driver.find_element_by_xpath("//input[@id='home-main-search']")
            if home_pages:
                #提前打标记
                account_results_coll.update_one({'_id': self.account_id}, {'$set': {"flag": 1}})
                self.flag=False
                return
        except Exception as e:
            # 如果找到登录页面元素，即账号不可用，登录失败
            try:
                no_use = self.driver.find_element_by_xpath("//div[@class='pb30 position-rel']/input")
                if no_use:
                    # 提前打标记
                    # 标记为不可用，下次不再取出
                    account_results_coll.update_one({'_id': self.account_id}, {'$set': {"usable": 1}})
                    return
            except Exception as e:
                # 获取列表页所有详情urls
                try:
                    tmp = self.driver.find_element_by_xpath('//span[contains(text(),"天眼查为你找到")]/..').text
                    match = int(re.search(r'天眼查为你找到(\d+)家公司',tmp).group(1))
                except Exception as e:
                    log.error(e)
                    match = 0
                if match:
                    self.parse_company_pages(match, log)
                    self.check_count = 0
                #都找不到说明没有进入列表页
                else:
                    try:
                        self.driver.find_element_by_xpath("//div[@class='container']//div[@class='content']")
                        self.image_handle(log)
                        # 提前打标记
                        updateTime = str(int(time.time() * 1000))
                        account_results_coll.update_one(
                            {'_id': self.account_id}, {'$set': {"flag": 0,'updateTime': updateTime }}
                        )
                        self.flag = True
                        self.login(log)
                    # 如果出现检索条件过大，或者账号暂时不可用
                    except Exception as e:
                        if '普通用户可查看100家公司，VIP会员可查看5000家公司' in self.driver.page_source:
                            # 提前打标记
                            account_results_coll.update_one({'_id': self.account_id}, {'$set': {"flag": 0}})
                            # self.search_name_from_mongo()
                            # self.get_name_to_search()
                        else:
                            try:
                                error_str = self.driver.find_element_by_xpath("//div[@class='f24 mb40 mt40 sec-c1 ']").text
                                if error_str == "抱歉，没有找到相关结果！":
                                    log.info("[ERROR]: 抱歉，没有找到相关结果！")
                                    # 继续搜索下一个名字
                                    # 更新名字数量
                                    name_results_coll.update_one(
                                        {'_id': self._id},{'$set': {"name_num": 0, "company_numm": 0}}
                                    )
                                    self.check_count += 1
                                    if self.check_count >=4:
                                        updateTime = str(int(time.time() * 1000))
                                        account_results_coll.update_one(
                                            {'_id': self.account_id}, {'$set': {"flag": 0,'updateTime':updateTime }})
                                        self.flag = True
                                        self.login(log)

                                    # 更新公司数量
                                    # self.db.name_results.update_one({'_id': self._id},{'$set': {"company_numm": 0}})
                                    # self.get_name_to_search()
                            except Exception as e:
                                # 匹配错误提示信息
                                error_info = self.driver.find_element_by_xpath("/html/body/div/div[1]").text
                                if error_info == "系统检测到您非人类行为，己被禁止访问天眼查，若有疑问请联系官方qq群 515982002":
                                    log.info("[ERROR]: {}".format(error_info))
                                    updateTime = str(int(time.time() * 1000))
                                    account_results_coll.update_one(
                                        {'_id': self.account_id}, {'$set': {"flag": 0,'updateTime':updateTime }})
                                    self.flag = True
                                    self.login(log)

    def parse_company_pages(self, match, log):
        '''
        遍历获取所有的限定条件
        :return:
        '''
        # 一级条件
        if match:
            print('当前公司数量：{}'.format(match))
            for province in self.province:
                pass



    def parse_condition(self, type, condition, log, pro=None):
        '''
        条件判断
        :param log:
        :return:
        '''
        data = []
        # 一级条件(全部省份)
        if type == 'first':
            for province in self.province:
                first_condition  = condition + '&{}'.format(redis_conn.rhget('city', province))
                url = 'https://www.tianyancha.com/search?{}'.format(first_condition)
                self.driver.get(url)
                time.sleep(2)
                try:
                    tmp = self.driver.find_element_by_xpath('//span[contains(text(),"天眼查为你找到")]/..').text
                    match = int(re.search(r'天眼查为你找到(\d+)家公司', tmp).group(1))
                except Exception as e:
                    log.error(e)
                    continue
                print('当前省份：{}, 公司数量：{}'.format(province.split('-')[0], match))
                data.append({'province': province.split('-')[0], 'match': match, 'url': url})
            return data if data else None
        # 二级条件（当前省份的所有城市）
        elif type == 'second':
            city_list = self.get_city(pro)
            for city in city_list:
                second_condition = condition + '&{}'.format(redis_conn.rhget('city', city))
                url = 'https://www.tianyancha.com/search?{}'.format(second_condition)
                self.driver.get(url)
                time.sleep(2)
                try:
                    tmp = self.driver.find_element_by_xpath('//span[contains(text(),"天眼查为你找到")]/..').text
                    match = int(re.search(r'天眼查为你找到(\d+)家公司', tmp).group(1))
                except Exception as e:
                    log.error(e)
                    continue
                print('当前城市：{}, 公司数量：{}'.format(city, match))
                data.append({'province': city.split('-')[1], 'match': match, 'url': url})
        # 三级条件（当前城市所有区域）
        elif type == 'third':
            pass


    def update_name_db(self, log):
        '''
        修改name_results字段
        :return:
        '''
        try:
            # 更新名字数量
            name_results_coll.update_one(
                {'_id': self._id}, {'$set': {"name_num": self.name_num, "company_numm": self.company_num}}
            )
            # log.info("数据更新中...")
        except Exception as e:
            log.info("数据无法更新...")

    def judge_num(self, no_sure_num, log):
        '''
        判断公司数量
        :return:
        '''
        # 普通账号只能爬小于100家的
        if no_sure_num <= 100:
            self.get_next_page(log)

    def get_next_page(self, log):
        '''
        翻页功能，获取列表页下一页
        :return:
        '''
        #计算总页数( 向上取整)
        company_page = math.ceil(self.company_num / 20)
        log.info("总页数：{}".format(company_page))
        data = []
        #拼接url
        for next_link in range(1,int(company_page)+1):
            # log.info("当前页码：{}".format(next_link))
            if next_link != 1:
                next_page_url = "https://www.tianyancha.com/search/p{}?key={}".format(next_link,self.label_name)
                self.driver.get(next_page_url)
                time.sleep(2)
            #解析页面
            item = self.parse_and_get_list_company(log)
            if item:
                data.extend(item)
        if data:
            insert_db(data, log)
            name_results_coll.update_one({'_id': self._id}, {'$set': {"flag": 1}})


    def parse_and_get_list_company(self, log):
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
            log.error('找不到所有的公司外层的模块{}'.format(e))
            account_results_coll.update_one({'_id': self.accunt_item['_id']}, {'$set': {"flag": 0}})
            self.driver.quit()
            quit()

        items = []

        for div in div_lists:
            dic={}
            try:
                tmp = div.find('a', attrs={'href': re.compile('https://www.tianyancha.com/company/\d+')})
                # 公司名称
                dic['companyName'] = tmp.get_text(strip=True)
                # 公司url
                dic['companyUrl'] = tmp.attrs['href']
            except Exception as e:
                log.error(e)
                continue
            # 经营状态
            try:
                dic['businessState'] = tmp.next_sibling.get_text(strip=True)
            except Exception:
                dic['businessState'] = ''
            # 公司所属省份
            try:
                dic['companyProvince'] = div.contents[2].get_text(strip=True)
            except Exception:
                dic['companyProvince'] = ''

            # 法人/注册资本/注册时间/联系电话/邮箱/法人信息
            tags = div.contents[1].contents[1:-1]
            data = []
            for tag in tags:
                for _ in tag.contents:
                    data.append(_.get_text(strip=True))
            # 对初步解析的文本进一步分割
            tmp_dic= {'法定代表人': 'legalMan',
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
                        dic['manUrl'] = div.find('a', attrs={'title': value}).attrs['href']
                    except Exception:
                        log.error('获取法人链接失败')
                if key in ['联系电话', '邮箱']:
                    try:
                        tel_lists = re.search('.*\[(.*)\].*', value.replace('\"', '')).group(1).split(',')
                    except Exception:
                        tel_lists = [value]
                    dic[tmp_dic[key]] = tel_lists
                else:
                    try:
                        dic[tmp_dic[key]] = value
                    except Exception:
                        pass
            items.append(dic)
            # 数据存储
        return items if items else False

        """---------"""

    def image_handle(self, log):
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
            newfont = ImageFont.truetype('simkai.ttf', 30)
            draw.text((5, 10), '按照下面文字顺序依次点击!!!', (255,0,255), font=newfont)
            del draw
            im.save('{}screenshot_{}{}.png'.format(self.img_path, 'normal_account',str(self.skip_count)))
            #调用验证码接口
            self.use_port(log)
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("[INFO]: 验证码图片存储失败")

    def use_port(self, log):
        '''
        调取打码平台接口
        :return:
        '''
        try:
            # import rk_python3
            get_data = rk_python3.identify('{}screenshot_{}{}.png'.format(self.img_path, 'normal_account',str(self.skip_count)))
            self.handle_auth(get_data, log)
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("验证码接口调用失败")

    def error_auth(self, log):
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

    def handle_auth(self,get_data, log):
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
            # self.handle_question()
        except Exception as e:
            log.info("[ERROR]: {}".format(e))
            log.info("验证码图片点击失败".format('{}screenshot_{}_{}.png'.format(self.img_path, 'normal_account',str(self.skip_count))))
            # 将打码错误信息返回给打码平台
            self.error_auth(log)
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
            self.use_port(log)

    def get_province(self):
        '''
        返回省份
        :return:
        '''
        return ([i.decode() for i in self.city_keys if '全部' in i.decode()])

    def get_city(self, province):
        '''
        返回省份对应的城市
        :param province: 省份
        :return:
        '''
        return ([i.decode() for i in self.city_keys if (province in i.decode()) and ('全部' not in i.decode())])

    def get_area(self, city):
        '''
        返回城市对应的地区
        :param city: 城市
        :return:
        '''
        return ([i.decode() for i in self.area_keys if (city in i.decode())])