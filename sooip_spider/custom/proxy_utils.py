import requests
from custom.mongo_utils import Database


class IpPool:
    def __init__(self, times=40):
        """
        初始化IP池参数
        :param times: IP使用次数
        """
        db = Database("mongodb://root:root962540@10.0.0.55:27017", "ip_db", maxSize=10)
        self.ip_col = db.make_col("ip_results")
        self.times = times
        self.counter = 0
        # 随机取出一个IP
        self.switch()

    def switch(self):
        """
        数据库获取IP
        :return:
        """
        self.ip = self.ip_col.random().get('ip')

    def count(self):
        """
        统计使用次数，次数到达规定上限从新选择IP
        :return:
        """
        self.counter += 1
        if self.counter >= self.times:
            self.switch()
            self.counter = 0

    def get(self, type="normal"):
        """允许返回3，normal, dict, http, https"""
        self.count()
        if type == 'normal':
            return self.ip
        elif type == 'dict':
            return {'https': 'https://' + self.ip, 'http': 'http://' + self.ip}
        elif type == 'http':
            return 'http://' + self.ip
        elif type == 'https':
            return 'https://' + self.ip
        else:
            raise ValueError('type parameter must be in [normal, dict, http, https] default normal')


class StaticIp:
    def __init__(self):
        db = Database("mongodb://root:root962540@10.0.0.55:27017", "ip_db", maxSize=10)
        self.ip_col = db.make_col("vps_static_ip_results")

    def gen_list(self):
        my_ip = ['10.0.0.55:9999', '10.0.0.52:9999', '10.0.0.54:9999', '10.0.0.50:9999', '10.0.0.53:9999']
        all_ip = [item['ip'] for item in self.ip_col.find()] + my_ip
        return all_ip

    def tester(self, ip):
        try:
            url = "https://www.baidu.com/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36"}
            proxy = {"https": ip, "http": ip}
            res = requests.get(url, headers=headers, proxies=proxy, timeout=1)
            if res.status_code == 200:
                return ip
        except Exception:
            pass

    def test_param(self, type):
        if type not in ['normal', 'dict', 'http', 'https']:
            raise ValueError('type parameter must be in [normal, dict, http, https] default normal')

    def get_ip_list(self, type="normal"):
        self.test_param(type)
        res = []
        ip_list = self.gen_list()
        for ip in ip_list:
            ip = self.tester(ip)
            if ip:
                func = 'self.' + type + '_type'
                item = eval(func)(ip)
                res.append(item)
        return res

    def normal_type(self, ip):
        return ip

    def dict_type(self, ip):
        return {"https": "https://" + ip, "http": "http://" + ip}

    def http_type(self, ip):
        return 'http://' + ip

    def https_type(self, ip):
        return 'http://' + ip

