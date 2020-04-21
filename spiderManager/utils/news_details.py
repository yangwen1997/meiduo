from time import sleep
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import pymongo
import hashlib
import re


class ToMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            'mongodb://rwuser:48bb67d7996f327b@10.0.0.120:57017,10.0.0.121:57017,10.0.0.122:57017/?replicaSet=rs1')

    def getUrls(self):
        '''取待爬取的urls'''
        db = self.client.jinritoutiao_com
        sheet = db.list_results
        urls = []
        for i in sheet.find({'is_crawl': False}).limit(300):
            one = {}
            one['url'] = i['url']
            one['id'] = i['_id']
            one['newsType'] = i['newsType']
            one['img'] = i['img']
            urls.append(one)
        print(urls)
        return urls

    def updateUrls(self, title, id):
        '''更新商标号的爬取状态'''
        db = self.client.jinritoutiao_com
        sheet = db.list_results
        sheet.update({'_id': id}, {'$set': {'is_crawl': True}})
        if title == '':
            print('数据结构错误, 无法抓取')
        print('已完成爬取: %s' % title)

    def saveToMongo(self, data, id, newsType, img):
        db = self.client.jinritoutiao_com
        sheet = db.detail_results
        data = data
        data['newsType'] = newsType
        data['titleImg'] = img
        sheet.insert(data)
        print('存入数据库: %s' % data['title'])
        self.updateUrls(data['title'], id)


class Toutiao(object):
    def __init__(self, ip):
        self.options = webdriver.ChromeOptions()
        # self.options.set_headless()
        # self.options.add_argument('--headless')
        # self.options.add_argument('--disable-gpu')
        self.options.add_argument("--proxy-server=http://" + ip)
        self.driver = webdriver.Chrome(options=self.options)

    def getData(self, url):
        self.driver.get(url)
        sleep(3)
        try:
            if self.driver.current_url.startswith('https://www.toutiao.com'):
                WebDriverWait(self.driver, 20).until(lambda x: x.find_element_by_xpath('//div[@class="article-box"]'))
                # 标题
                title = self.driver.find_element_by_xpath('//div[@class="article-box"]/h1[@class="article-title"]').text
                h1 = hashlib.md5()
                h1.update(title.encode(encoding='utf-8'))
                id = h1.hexdigest()
                # print(title)
                # 时间
                articleSub = self.driver.find_element_by_xpath('//div[@class="article-box"]/div[@class="article-sub"]').text
                articleSub = articleSub.replace('原创', '').strip()
                # print(articleSub)
                f = articleSub.strip().split(' ')
                b = []
                b.append(f[-2])
                b.append(f[-1])
                pubdate = 'T'.join(b)
                # 简介
                try:
                    part = self.driver.find_element_by_xpath('//div[@class="article-content"]/p[1]').text
                    if re.search('图片来源', part) is not None:
                        part = self.driver.find_element_by_xpath('//div[@class="article-content"]//p[2]').text
                except Exception as e:
                    print(e)
                    try:
                        part = self.driver.find_element_by_xpath('//div[@class="article-content"]//p[2]').text
                        if len(part) <= 15:
                            part = ''
                    except Exception as e:
                        print(e)
                        part = self.driver.find_element_by_xpath('//div[@class="article-content"]//p[1]').text
                        if len(part) <= 15:
                            part = ''
                # 正文
                content = self.driver.find_element_by_xpath('//div[@class="article-box"]/div[@class="article-content"]').get_attribute('innerHTML')
                # print(content)
                data = {'_id': id, 'title': title, 'pubdate': pubdate, 'articleSub': articleSub, 'part': part, 'content': content}
                return data
            else:
                return None
        except TimeoutException as e:
            print(e)
            return None

    def run(self, url):
        data = self.getData(url)
        self.driver.close()
        return data


def details_run():
    mongo = ToMongo()
    urls = mongo.getUrls()
    for url in urls:
        toutiao = Toutiao('10.0.0.52:9999')
        data = toutiao.run(url['url'])
        # print(data)
        if data is not None:
            try:
                mongo.saveToMongo(data, url['id'], url['newsType'], url['img'])
            except DuplicateKeyError as e:
                print(e)
                continue
        else:
            mongo.updateUrls('', url['id'])
