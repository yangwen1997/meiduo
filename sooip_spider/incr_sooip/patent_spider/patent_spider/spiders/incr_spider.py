# -*- coding: utf-8 -*-
import re
import hashlib
from functools import partial

import scrapy

from patent_spider.utils.common import *
from patent_spider.utils.param import *


class IncrSpiderSpider(scrapy.Spider):
    name = 'incr_spider'
    handle_httpstatus_list = [404]
    list_url = "http://www.sooip.com.cn/txnPatentData01.ajax"
    detail_url = "http://www.sooip.com.cn/app/patentdetail?pid="
    law_url = "http://www.sooip.com.cn/app/lawdetail?pid="

    MAP = {'CLA': 'CLA/CLA_ZH.html',
           'DES': 'DES/DES_ZH.html'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = RFPDupeFilter()

    def start_requests(self):
        date = '20190118'
        yield scrapy.FormRequest(self.list_url, formdata=list_param(date), meta={'date': date}, dont_filter=True)

    def parse(self, response):
        date = response.meta.get('date')
        total = count_total(response.text)
        for start in compute(total):
            yield scrapy.FormRequest(self.list_url, formdata=list_param(date, start),
                                     callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        nodes = re.findall(r'<patent>(.*?)</patent>', response.text, re.S)
        for node in nodes:
            extract = partial(extract_by_re, node)
            pid = extract('<PID>(\w*?)</PID>')
            ano = extract('<ANO>(.*?)</ANO>')
            if '.' in ano:
                ano = ano.split('.')[0]
            abs = extract('<ABSO>(.*?)</ABSO>') or extract('<DEBEO>(.*?)</DEBEO>')
            raw_drap = extract('<DRAP>(.*?)</DRAP>')
            drap = deal_drap(raw_drap)
            item = {'_id': hashlib.md5(ano.encode('utf8')).hexdigest(),
                    'applyCode': ano,
                    'absInfo': abs,
                    'desDrawings': drap,
                    'pid': pid}
            detail_url = self.detail_url + pid
            if not self.filter.request_seen(pid):
                yield scrapy.Request(detail_url, meta={'item': item}, callback=self.parse_detail,
                                     dont_filter=True, priority=50)

    def parse_detail(self, response):
        item = response.meta.get('item')
        inventName = response.xpath('//*[@class="jsxq_tit"]/text()').extract_first().strip()  # 发明名称

        patType = response.xpath('//*[@class="jsclass"]//div/text()').extract()  # 状态

        applyVerifyCode = response.xpath('//th[contains(text(), "申请号：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 申请校验号

        applyDate = response.xpath('//th[contains(text(), "申请日：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 申请日

        publicCode = response.xpath('//th[contains(text(), "公开(公告)号：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 公开(公告)号
        publicDate = response.xpath('//th[contains(text(), "公开(公告)日：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 公开(公告)日

        applicant = response.xpath('//th[contains(text(), "申请人：")]/following-sibling::td[1]/span/text()'). \
            extract_first().strip()  # 申请人
        inventor = response.xpath('//th[contains(text(), "发明人：")]/following-sibling::td[1]/span/text()'). \
            extract_first().strip()  # 发明人
        address = response.xpath('//th[contains(text(), "申请人地址：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 申请人地址
        areaCode = response.xpath('//th[contains(text(), "申请人区域代码：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 申请人区域代码
        patentee = response.xpath('//th[contains(text(), "专利权人：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()

        zjnClassify = response.xpath('//th[contains(text(), "洛迦诺分类：")]/following-sibling::td[1]/span/text()'). \
            extract_first().strip()  # 洛迦诺分类

        IPCCode = response.xpath('//th[contains(text(), "IPC：")]/following-sibling::td[1]/span/text()'). \
            extract_first().strip()  # IPC 分类号

        CPCCode = response.xpath('//th[contains(text(), "CPC：")]/following-sibling::td[1]/span/text()'). \
            extract_first().strip()  # CPC

        priority = response.xpath('//th[contains(text(), "优先权：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 优先权

        patAgency = response.xpath('//th[contains(text(), "专利代理机构：")]/following-sibling::td[1]/span/text()'). \
            extract_first().strip()  # 专利代理机构
        patAgent = response.xpath('//th[contains(text(), "代理人：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 代理人

        examiner = response.xpath('//th[contains(text(), "审查员：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 审查员

        gjsq = response.xpath('//th[contains(text(), "国际申请：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 国际申请

        gjgk = response.xpath('//th[contains(text(), "国际公开（公告）：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 国际公开（公告）

        jrgjrq = response.xpath('//th[contains(text(), "进入国家日期：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 进入国家日期

        fasq = response.xpath('//th[contains(text(), "分案申请：")]/following-sibling::td[1]/text()'). \
            extract_first().strip()  # 分案申请

        keyWords = response.xpath('//ul[@class="keyWordUL"]//li/span/text()').extract()  # 关键词

        loadPath = response.xpath('//input[@id="loadPath"]/@value').extract_first()  # 内页链接

        data = {
            '_id': item['_id'],
            'inventName': inventName,
            'applyCode': item['applyCode'],
            'detailSource': 'sooip',
            'docs': {
                'baseInfo': {
                    'applyVerifyCode': applyVerifyCode,
                    'applyDate': applyDate,
                    'publicCode': publicCode,
                    'publicDate': publicDate,
                    'applicant': applicant,
                    'inventor': inventor,
                    'address': address,
                    'areaCode': areaCode,
                    'patentee': patentee,
                    'zjnClassify': zjnClassify,
                    'IPCCode': IPCCode,
                    'CPCCode': CPCCode,
                    'priority': priority,
                    'patAgency': patAgency,
                    'patAgent': patAgent,
                    'examiner': examiner,
                    'gjsq': gjsq,
                    'gjgk': gjgk,
                    'jrgjrq': jrgjrq,
                    'fasq': fasq
                },
                'patType': patType,
                'imgUrls': {
                    'desDrawings': item['desDrawings'],
                },
                'keyWords': keyWords,
                'absInfo': item['absInfo']
            },
        }
        law_url = self.law_url + item['pid']
        yield scrapy.Request(url=law_url, meta={'data': data, 'loadPath': loadPath}, callback=self.parse_law, priority=70)

    def parse_law(self, response):
        data = response.meta.get('data')
        loadPath = response.meta.get('loadPath')
        lawInfo = []
        nodes = response.xpath('//div[@class="fvztzt"]/table/tr')
        for node in nodes:
            lawDate = node.xpath('td[1]/span/text()').extract_first()
            lawStatus = node.xpath('td[2]/text()').extract_first().strip()
            lawStatusInfo = node.xpath('td[3]/text()').extract_first().strip()
            item = {'lawDate': lawDate, 'lawStatus': lawStatus, 'lawStatusInfo': lawStatusInfo}
            lawInfo.append(item)
        data['docs']['lawInfo'] = lawInfo
        abs_url = loadPath + self.MAP.get('CLA')
        yield scrapy.Request(url=abs_url, meta={'data': data, 'loadPath': loadPath}, callback=self.parse_cla, priority=80)

    def parse_cla(self, response):
        pattern = re.compile('<div class="Section1">.*</div>', re.S)
        data = response.meta.get('data')
        loadPath = response.meta.get('loadPath')

        if response.status == 404:
            data['docs']['claInfo'] = ''
            data['docs']['imgUrls']['claImg'] = []
            des_url = loadPath + self.MAP.get('DES')
            yield scrapy.Request(url=des_url, meta={'data': data, 'loadPath': loadPath}, callback=self.parse_des,
                                priority=100)
        else:
            cla_text = response.text
            img_list = response.xpath('//img/@src').extract()
            if len(img_list) > 0:
                claImg = [loadPath + 'CLA/' + img for img in img_list]
            else:
                claImg = []

            data['docs']['claInfo'] = pattern.search(cla_text).group()
            data['docs']['imgUrls']['claImg'] = claImg

            des_url = loadPath + self.MAP.get('DES')
            yield scrapy.Request(url=des_url, meta={'data': data, 'loadPath': loadPath}, callback=self.parse_des, priority=100)

    def parse_des(self, response):
        pattern = re.compile('<div class="Section1">.*</div>', re.S)
        data = response.meta.get('data')
        loadPath = response.meta.get('loadPath')
        if response.status == 200:
            des_text = response.text
            img_list = response.xpath('//img/@src').extract()
            if len(img_list) > 0:
                desImg = [loadPath + 'DES/' + img for img in img_list]
            else:
                desImg = []
            data['docs']['desInfo'] = pattern.search(des_text).group()
            data['docs']['imgUrls']['desImg'] = desImg
        elif response.status == 404:
            data['docs']['desInfo'] = ''
            data['docs']['imgUrls']['desImg'] = []
        data['flag'] = 0
        yield data