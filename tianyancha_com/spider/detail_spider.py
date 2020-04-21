import os
import time
import logging as log
import datetime
from PIL import Image,ImageFont,ImageDraw
from selenium import webdriver
from bs4 import BeautifulSoup as B
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import sys
sys.path.append(r"D:\projects\04_Coding\spider")
import core as C


class DownReportSpider(object):
    def __init__(self, img_path):
        self.client = C.mongo_client()
        self.tyc_db = self.client['tyc_com']
        self.all_com_db = self.client['all_com']
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        # 设置下载路径
        chrome_options.add_argument("--proxy-server=http://10.0.0.54:9999")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get('https://www.tianyancha.com/login')
        self.driver.delete_all_cookies()
        cookies = [
            {'domain': '.tianyancha.com', 'expiry': 2145931345, 'httpOnly': False, 'name': 'ssuid', 'path': '/', 'secure': False, 'value': '1493837298'},
            {'domain': 'www.tianyancha.com', 'httpOnly': True, 'name': 'aliyungf_tc', 'path': '/', 'secure': False, 'value': 'AQAAADLm+hRMxwYAVmu5binAOGDd6g3E'},
            {'domain': '.tianyancha.com', 'expiry': 1533960150, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.529871592.1533873747'},
            {'domain': '.tianyancha.com', 'expiry': 1596945750, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.1410567175.1533873747'},
            {'domain': 'www.tianyancha.com', 'httpOnly': False, 'name': 'csrfToken', 'path': '/', 'secure': True, 'value': 'jtOFeU3rU5v7U6r8RLjALuOx'},
            {'domain': '.tianyancha.com', 'expiry': 1596945741.177792, 'httpOnly': True, 'name': 'TYCID', 'path': '/', 'secure': False, 'value': '290a1ca09c5211e8a542bd107d2ed947'},
            {'domain': '.tianyancha.com', 'expiry': 1533873806, 'httpOnly': False, 'name': '_gat_gtag_UA_123487620_1', 'path': '/', 'secure': False, 'value': '1'},
            {'domain': '.tianyancha.com', 'expiry': 1596945741.177825, 'httpOnly': True, 'name': 'undefined', 'path': '/', 'secure': False, 'value': '290a1ca09c5211e8a542bd107d2ed947'},
            {'domain': '.tianyancha.com', 'expiry': 1565409750, 'httpOnly': False, 'name': 'Hm_lvt_e92c8d65d92d534b0fc290df538b4758', 'path': '/', 'secure': False, 'value': '1533873745'},
            {'domain': '.tianyancha.com', 'expiry': 1534478549, 'httpOnly': False, 'name': 'tyc-user-info', 'path': '/', 'secure': False, 'value': '%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTc2NTAyNDU3NSIsImlhdCI6MTUzMzg3MzczOSwiZXhwIjoxNTQ5NDI1NzM5fQ._rUZL0trqWxjvRJaHKxBwPZHXQFe8t6Lw1htHxzGKQ6bzf0KbXwRrjcRfGKQFDyv8i5Xgpq6vdefjq6G2H0cjQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%252240%2522%252C%2522mobile%2522%253A%252215765024575%2522%257D'},
            {'domain': '.tianyancha.com', 'expiry': 1534478549, 'httpOnly': False, 'name': 'auth_token', 'path': '/', 'secure': False, 'value': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTc2NTAyNDU3NSIsImlhdCI6MTUzMzg3MzczOSwiZXhwIjoxNTQ5NDI1NzM5fQ._rUZL0trqWxjvRJaHKxBwPZHXQFe8t6Lw1htHxzGKQ6bzf0KbXwRrjcRfGKQFDyv8i5Xgpq6vdefjq6G2H0cjQ'},
            {'domain': '.tianyancha.com', 'httpOnly': False, 'name': 'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758', 'path': '/', 'secure': False, 'value': '1533873750'}]
        for _ in cookies:
            self.driver.add_cookie(_)
        self.used_account = []
        self.account_num = None
        self.img_path = img_path
        self.password = None
        self.flag = True
        self.check_num = 0
        self.tmp_num = 0



    def run(self):
        # self.login()
        self.detail_parse("https://www.tianyancha.com/company/23402373")
        # while True:
        #     # res = self.get_company()
        #     if res:
        #         for _ in res:
        #             # 下载报告解析
        #             try:
        #                 self.detail_parse(_)
        #             except Exception as e:
        #                 log.error(e)
        #                 log.error('详情爬取失败')
        #     else:
        #         log.info('没有符合条件的公司\n')
        #         break

    # 详情解析
    def detail_parse(self, url):
        # url = company_dic.get('companyUrl')
        self.driver.get(url)
        time.sleep(3)
        # print(self.driver.page_source)
        try:
            html = B(str(self.driver.page_source), 'lxml')
            header_html = html.find('div', class_='detail')
        except Exception as e:
            log.error('获取头部信息失败 {}'.format(e))
            return
        divs = header_html.find_all('div', class_='in-block')
        header_data = {}
        # 公司logo
        try:
            header_data['clUrl'] = html.find('div', class_='logo -w100').attrs['data-src']
        except Exception:
            pass
        # 曾用名
        try:
            header_data['usedName'] = html.find('div', class_='history-content').get_text(strip=True)
        except Exception:
            pass
        # 上市信息
        try:
            # 股票板块
            header_data['plate'] = html.find('span', class_='line').get_text()
            bond = html.find('span', class_='bond').get_text()
            bond_name = html.find('span', class_='bond_name').get_text()
            # 股票代号
            header_data['stockNum'] = bond + bond_name
        except Exception:
            pass
        # 头部基本信息
        header_dic = {
            '电话：': 'companyTel',
            '邮箱': 'companyEmail',
            '网址': 'companyWebeUrl',
            '地址': 'registerAddress',
            '简介': 'companyBrief',
        }
        for name, value in header_dic:
            try:
                if '网址' in name:
                    header_data[value] = divs.find('span',text='网址：').find('a').get_text(strip=True)
                else:
                    header_data[value] = divs.find('span', text=name).find('script', attrs={'type': 'text/html'}).get_text(strip=True)
            except Exception:
                pass

        """工商信息"""
        base_data = {}
        try:
            tables = html.find('div',id='_container_baseInfo').find_all('table')
        except Exception:
            log.error('工商信息获取失败')
            return

        # 法人及法人logo
        try:
            base_data['legalMan'] = tables[0].find('div',class_='humancompany').get_text(strip=True)
            base_data['mlUrl'] = tables[0].find('div',class_='lazy-img -image').img.attrs['data-src']
        except Exception:
            pass

        # 注册资本
        try:
            base_data['registerMoney'] = tables[0].find_all('tr', recursive=False)[0].find_all('td',recursive=False)[1].find_all('div',recursive=False)[1].attrs['title']
        except Exception:
            pass

        # 注册时间
        try:
            # base_data['registerTime']
            registerTimes  = tables[0].find_all('tr', recursive=False)[1].td.find_all('div',recursive=False)[1].get_text(strip=True).split('-')
            for registerTime in registerTimes:
                for _ in registerTime:
        except Exception:
            pass







    # 获取账号
    def get_account_from_db(self):
        self.account_num = 15765024575
        self.password = 'a123456789'
        # res = self.tyc_db['account_results'].find_one({"account_rank": 0,"usable": 0,"flag": 0})
        # if res:
        #     #  账号标记为占用
        #     self.tyc_db['account_results'].update_one({'account_name': res.get('account_name')}, {'$set': {'flag': 1}})
        #     self.account_num = res.get('account_name')
        #     self.password = res.get('password')
        #     log.info('当前账号：[{}]'.format(self.account_num))
        # else:
        #     log.info('没有符合的账号')
        #     quit()

    # 获取公司
    def get_company(self):
        res = self.all_com_db['all_results'].find(
            {
                "companyUrl": {'$ne': ''},
                "allTime.usedWeb.qichacha_com.getTime": 0,
                "allTime.usedWeb.tyc_com.getTime": 0,
                "allTime.usedWeb.qixin_com.getTime": 0,
                "allTime.usedWeb.gxzg_com.getTime": 0,
                "allTime.usedWeb.weimao_com.getTime": 0,
                "allTime.usedWeb.eqicha_com.getTime": 0,
                'reportFlag': 0
            }
        ).limit(100)
        lists = []
        for _ in res:
            # 设置取出数据的时间
            getTime = str(int(time.time() * 1000))
            self.all_com_db['all_results'].update_one(
                {'_id': _.get('_id')},
                {'$set': {
                    'reportFlag': 1,
                    "allTime.usedWeb.tyc_com.getTime": getTime
                }}
            )
            lists.append(_)
        return lists

    def login(self):
        '''
        登录
        :return:
        '''
        login_url = "https://www.tianyancha.com/login"
        while self.flag:
            try:
                self.driver.get(login_url)
                time.sleep(2)
                # 获取账号
                self.get_account_from_db()
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
                log.error("{}".format(e))
                log.error("登录失败")
                # 将账号释放，重新登陆
                self.tyc_db['account_results'].update_one({'account_name': self.account_num}, {'$set': {'flag': 0}})
                quit()

    def handle_question(self,):
        '''
        判断是否登录成功
        :return:
        '''
        try:
            #如果跳转到首页即登录成功
            home_pages = self.driver.find_element_by_xpath("//input[@id='home-main-search']")
            if home_pages:
                self.flag = False
                cookie = self.driver.get_cookies()
                print (cookie)
                return
        except Exception as e:
            # 如果找到登录页面元素，即账号不可用，登录失败
            try:
                no_use = self.driver.find_element_by_xpath("//div[@class='pb30 position-rel']/input")
                if no_use:
                    # 将账号释放，重新登陆
                    self.tyc_db['account_results'].delete_one({'account_name': self.account_num})
            except Exception as e:
                try:
                    self.driver.find_element_by_xpath("//div[@class='container']//div[@class='content']")
                    self.image_handle()
                except Exception as e:
                    # 匹配错误提示信息
                    error_info = self.driver.find_element_by_xpath("/html/body/div/div[1]").text
                    if error_info == "系统检测到您非人类行为，己被禁止访问天眼查，若有疑问请联系官方qq群 515982002":
                        log.error("{}".format(error_info))
                        # 将账号释放，重新登陆
                        self.tyc_db['account_results'].update_one({'account_name': self.account_num}, {'$set': {'flag': 0}})

    def image_handle(self):
        '''
        验证码处理
        :return:
        '''
        self.driver.get_screenshot_as_file('{}img_down_report.png'.format(self.img_path))
        #获取验证码元素的坐标
        captchaElem = self.driver.find_element_by_xpath("//div[@class='new-box94']")
        #获取验证码元素的大小
        left = int(captchaElem.location['x'])
        top = int(captchaElem.location['y'])
        right = int(captchaElem.location['x'] + captchaElem.size['width'])
        bottom = int(captchaElem.location['y'] + captchaElem.size['height'])
        try:
            #打开
            image_info = Image.open('{}img_down_report.png'.format(self.img_path))
            im = image_info.crop((left,top,right,bottom))
            #编辑
            draw = ImageDraw.Draw(im)
            ##设置字体
            newfont = ImageFont.truetype('simkai.ttf', 30)
            draw.text((5, 10), '按照下面文字顺序依次点击!!!', (255,0,255), font=newfont)
            del draw
            im_name = im.save('screenshot_{}.png'.format('down_report'))
            #调用验证码接口
            self.use_port()
        except Exception as e:
            print("[ERROR]: {}".format(e))
            print("[INFO]: 验证码图片存储失败")

    def use_port(self):
        '''
        调取打码平台接口
        :return:
        '''
        try:
            import rk_python3
            get_data = rk_python3.identify('{}screenshot_{}.png'.format(self.img_path, 'down_report'))
            self.handle_auth(get_data)
        except Exception as e:
            print("[ERROR]: {}".format(e))
            print("验证码接口调用失败")

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
            print("[ERROR]: 错误id返回平台成功：{}".format(get_error_data))
        except Exception as e:
            print("[ERROR]: {}".format(e))
            print("错误id返回平台失败")

    def handle_auth(self,get_data):
        '''
        接口返回数据进行处理，进行验证码点击
        :return:
        '''
        try:
            # #下次图片命名以2、3、4.。。。
            index_data = get_data["Result"]
            self.error_id = get_data["Id"]
            print("[INFO]: 获取到的验证码坐标:{}".format(index_data))
            print("[INFO]: 获取到的验证码id:{}".format(self.error_id))
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
            print("[ERROR]: {}".format(e))
            print("验证码图片点击失败".format('screenshot_{}.png'.format('down_report')))
            # 将打码错误信息返回给打码平台
            self.error_auth()
            #记录
            with open("error_auth_image.txt", "a", encoding="utf-8") as f:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(now_time)
                f.write("\n")
                f.write(str('screenshot_{}.png'.format('down_report')))
                f.write("\n")
                f.write("\n")
            f.close()
            #再次调用接口
            self.use_port()

if __name__=='__main__':
    realpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/log/"
    imgpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/img/"
    fdf_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/pdf/"
    filename = "{}down_report_debug_{}.log".format(realpath, time.strftime("%Y-%m-%d", time.localtime()))

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

    base = DownReportSpider(imgpath)
    base.run()