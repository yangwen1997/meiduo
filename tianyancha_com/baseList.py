# -*- coding: utf-8 -*-
import logging
from selenium.webdriver import Chrome
from pymongo import MongoClient
from selenium.webdriver import ChromeOptions


logger = logging.getLogger(__name__)
IP_MONGO_URI = "mongodb://root:root962540@10.0.0.55:27017"


class ChromeBase:
    client = MongoClient(IP_MONGO_URI)
    col = client["ip_db"]["vps_static_ip_results"]
    _driver = None
    def __init__(self,mac=None):
        self.mac = mac
        self.dr = self.set_driver(self.mac)

    def set_driver(self,mac):
        if self._driver is None:
            options = ChromeOptions()
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-extensions')
            options.add_argument('--profile-directory=Default')
            options.add_argument('--incognito')
            proxy = self.col.find_one({"mac":mac})
            if proxy:
                options.add_argument("--proxy-server=http://{}".format(proxy))
            options.add_argument('lang=zh_CN.UTF-8')
            options.add_argument(
                'user-agent=Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20')
            self._driver = Chrome(chrome_options=options)
            self._driver.set_window_size(200, 800)

        return self._driver

    def run(self,*args,**kwargs):
        self.dr = self.set_driver(self.mac)
        pass

    def start(self):
        while True:
            try:
                self.run()
            except:
                self.on_failure()
    
    def on_failure(self):
        try:
            self._driver.quit()
        except:pass
        self._driver = None


