import os
import time
import logging as log
import datetime
from PIL import Image,ImageFont,ImageDraw
from selenium import webdriver
import hashlib
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import sys
sys.path.append(r"D:\projects\04_Coding\spider")
import core as C
from read_company_api import ReadCompanyApi


class DownReportSpider(object):
    def __init__(self, pdf_path, img_path):
        self.client = C.mongo_client()
        self.tyc_db = self.client['tyc_com']
        self.all_com_db = self.client['all_com']
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-infobars')
        # 设置下载路径
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': pdf_path}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--proxy-server=http://10.0.0.51:9999")
        path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
        self.used_account = []
        self.account_num = None
        self.img_path = img_path
        self.password = None
        self.flag = True
        self.check_num = 0
        self.tmp_num = 0


    def run(self):
        self.login()
        # self.down_report_parse({'companyName': '阿里', 'companyUrl': 'https://www.tianyancha.com/orderReport/0?rp=0&cid=4584507'})
        # report_url = "https://www.tianyancha.com/orderReport/0?rp=0&cid=4584507"
        api = ReadCompanyApi()
        # 获取公司
        while True:
            res = self.get_company(api)
            if res:
                for _ in res:
                    # 下载报告解析
                    try:
                        self.down_report_parse(_)
                    except Exception as e:
                        pass
                # 将不能下载报告的reportFlag标记为改为3
                for _ in res:
                    api.not_support_down_report(_.get('_id'))
            else:
                log.info('没有符合条件的公司\n')
                break

    # 下载报告解析
    def down_report_parse(self, company_dic):
        report_url = "https://www.tianyancha.com/orderReport/0?rp=0&cid={}".format(company_dic.get('companyUrl').split('/')[-1])
        while True:
            try:
                self.driver.get(report_url)
                time.sleep(1)
                # print(self.driver.page_source)
                js = "window.scrollTo(0,document.body.scrollHeight)"
                self.driver.execute_script(js)
                # 点击PDF格式
                self.driver.find_element_by_xpath("//div[@class='order-report-bottom new-border-top']/span[2]/label[1]/input").click()
                # 提交订单
                self.driver.find_element_by_id('commit').click()
                time.sleep(1)
                # 找不到查看订单说明今天的已经到上限了，需要登陆下一个账号
                if 'orderpay' in self.driver.current_url:
                    self.check_num +=1
                    break
                else:
                    if self.check_num <=9:
                        self.tmp_num += 1
                        if self.tmp_num <= 2:
                            break
                    """先将这个账号的报告都下载了"""
                    # 查看订单
                    time.sleep(5)
                    self.driver.get('https://www.tianyancha.com/usercenter/myorder')
                    time.sleep(1)
                    # self.driver.find_element_by_xpath('//div[@class="order-body"]/div[2]/div[1]').click()
                    elements = self.driver.find_elements_by_xpath("//div[@class='resemtable']/div[@class='resem-body pb27']/div[2]/div")
                    for i in elements:
                        element_down = i.find_element_by_xpath("div[@class='pull-right']/span[2]")
                        # 公司名称
                        element_title = i.find_element_by_xpath("span").text.strip()
                        # 修改名录reportFlag状态为下载完成,暂时改为2，后期需要改为1
                        m = hashlib.md5(element_title.encode(encoding='utf-8'))
                        change_name = m.hexdigest()
                        update_id = self.all_com_db['all_results'].update_one(
                            {'_id': change_name},
                            {'$set': {
                                'reportFlag': 2,
                                "allTime.usedWeb.tyc_com.getTime": str(int(time.time() * 1000))
                            }}
                        ).modified_count
                        if not update_id:
                            log.info('{} 修改名录状态失败'.format(element_title))
                        else:
                            log.info('{} update ID: [{}]'.format(element_title, update_id))
                            log.info('[{}] 报告下载中...'.format(element_title))
                            try:
                                element_down.click()
                            except Exception:
                                js = "window.scrollTo(0,500)"
                                self.driver.execute_script(js)
                                try:
                                    element_down.click()
                                except Exception:
                                    js = "window.scrollTo(500,1000)"
                                    self.driver.execute_script(js)
                                    try:
                                        element_down.click()
                                    except Exception:
                                        js = "window.scrollTo(0,0)"
                                        self.driver.execute_script(js)
                                        element_down.click()
                            time.sleep(0.3)
                            for _  in range(3):
                                try:
                                    self.driver.find_element_by_link_text('确    定').click()
                                    break
                                except Exception as e:
                                    log.error(e)
                                    time.sleep(2)
                                    pass
                            time.sleep(0.5)
            except Exception:
                self.handle_question()
            # 将这个账号写入已经用过的used_account.txt
            with open('used_account.txt','a+') as f:
                f.write('{}\n'.format(self.account_num))
            log.info('账号【{}】次数已经使用完\n'.format(self.account_num))
            self.check_num = 0
            self.tmp_num = 0
            # 释放账号
            self.tyc_db['account_results'].update_one({'account_name': self.account_num}, {'$set': {'flag': 0}})
            """重新登陆获取新的账号"""
            self.flag = True
            self.login()
            """"""
    # 获取账号
    def get_account_from_db(self):
        with open('used_account.txt', 'r') as f:
            for line in f.readlines():
                self.used_account.append(int(line.strip()))
        res = self.tyc_db['report_account_results'].find_one({"account_rank": 0,"usable": 0,"flag": 0, 'account_name':{'$nin':self.used_account}})
        if res:
            #  账号标记为占用
            self.tyc_db['report_account_results'].update_one({'account_name': res.get('account_name')}, {'$set': {'flag': 1}})
            self.account_num = res.get('account_name')
            self.password = res.get('password')
            log.info('当前账号：[{}]'.format(self.account_num))
        else:
            log.info('没有符合的账号')
            quit()

    # 获取公司
    def get_company(self, api):
        # 缓存中拿数据
        res = api.read_company_from_redis('tyc_com')
        for _ in res:
            # 下载报告前修改状态
            api.not_finish_to_update(_.get('_id'), 'tyc_com', is_report=True)
        return res

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

    base = DownReportSpider(fdf_path,imgpath)
    base.run()