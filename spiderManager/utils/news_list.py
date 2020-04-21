from time import sleep
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pymongo
import hashlib


def save_to_mongo(url, newsType, img):
    client = pymongo.MongoClient(
        'mongodb://rwuser:48bb67d7996f327b@10.0.0.120:57017,10.0.0.121:57017,10.0.0.122:57017/?replicaSet=rs1')
    db = client.jinritoutiao_com
    sheet = db.list_results
    h1 = hashlib.md5()
    h1.update(url.encode(encoding='utf-8'))
    toutiao_id = h1.hexdigest()
    sheet.insert({'_id': toutiao_id, 'img':img, 'newsType': newsType, 'form': 'toutiao.com', 'url': url, 'is_crawl': False})
    print('存储到MongoDB成功: 头条: ' + url)


def get_url(newsType):
    options = webdriver.ChromeOptions()
    # options.set_headless()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument("--proxy-server=http://10.0.0.52:9999")
    driver = webdriver.Chrome(options=options)
    try:
        if newsType == 'recommend':
            url = 'https://www.toutiao.com/'
            driver.get(url)
            WebDriverWait(driver, 50).until(lambda x: x.find_element_by_xpath('//div[@class="feed-infinite-wrapper"]'))
            # 将滚动条滚到页面底部
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            sleep(3)
            urls = driver.find_elements_by_xpath('//div[@class="feed-infinite-wrapper"]//ul/li')
            for i in range(1, len(urls) + 1):
                try:
                    url = driver.find_element_by_xpath('//div[@class="feed-infinite-wrapper"]//ul/li[%d]//div[@class="bui-left single-mode-lbox"]/a' % i).get_attribute('href')
                    img = driver.find_element_by_xpath('//div[@class="feed-infinite-wrapper"]//ul/li[%d]//div[@class="bui-left single-mode-lbox"]/a/img' % i).get_attribute('src')
                    # print(img)
                    # print('*****************************')
                    if url.startswith(r'https://www.toutiao.com/group/') and img.startswith(r'https://'):
                        try:
                            save_to_mongo(url, newsType, img)
                        except DuplicateKeyError as e:
                            print(e)
                            continue
                except Exception:
                    continue
        else:
            url = 'https://www.toutiao.com/ch/%s/' % newsType
            driver.get(url)
            WebDriverWait(driver, 50).until(lambda x: x.find_element_by_xpath('//div[@class="feedBox"]'))
            # 将滚动条滚到页面底部
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            sleep(10)
            urls = driver.find_elements_by_xpath('//div[@class="feedBox"]//ul/li')
            # print(urls)
            for i in range(1, len(urls) + 1):
                try:
                    url = driver.find_element_by_xpath('//div[@class="feedBox"]//ul/li[%d]//div[@class="lbox"]/a' % i).get_attribute('href')
                    # print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
                    img = driver.find_element_by_xpath('//div[@class="feedBox"]//ul/li[%d]//div[@class="lbox"]/a/img' % i).get_attribute('src')
                    if url.startswith(r'https://www.toutiao.com/group/') and img.startswith(r'https://p'):
                        try:
                            save_to_mongo(url, newsType, img)
                        except DuplicateKeyError as e:
                            print(e)
                            continue
                except Exception:
                    continue
    finally:
        driver.quit()


def list_run():
    newsTypes = ['recommend', 'news_hot', 'news_tech', 'news_entertainment', 'news_game', 'news_sports', 'news_car', 'news_finance', 'funny']
    # newsTypes = ['recommend']
    for i in range(2):
        for newsType in newsTypes:
            get_url(newsType)
