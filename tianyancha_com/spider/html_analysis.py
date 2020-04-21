import os
import re
import logging as log
import time
from bs4 import BeautifulSoup as B

class HtmlAnalysis(object):
    def __init__(self):
        pass

    # 主程序入口
    def run(self):
        # 读取html文件
        html = self.read_html()
        # 解析html
        self.parse(html)

    # 读取html文件
    def read_html(self):
        with open('tyc.html', 'r', encoding='utf-8') as f:
            html = B(f.read(), 'html.parser', )
        return html

    # 解析html
    def parse(self, html):

        # 截取出一级的目录
        first_level_tags = [str(_) for _ in html.find_all('h2')]
        all_tags = []
        # 企业背景、股东信息、对外投资信息等每个大模块之间的html(用正则解析两个h2标签中的html)
        for i in range(len(first_level_tags)):
            if i == len(first_level_tags) - 1:
                first_pattern_str = '({}.*)'.format(first_level_tags[i])
            else:
                first_pattern_str = '({}.*?){}'.format(first_level_tags[i], first_level_tags[i + 1])
            first_level_html = re.search(first_pattern_str, str(html)).group(1)
            # print(first_level_html)

            # 找到二级目录的标签
            second_level_tags = [str(_) for _ in B(first_level_html, 'html.parser').find_all('h3')]
            for j in range(len(second_level_tags)):
                # print(j)
                # print(len(second_level_tags))
                if j == len(second_level_tags) - 1:
                    second_pattern_str = '({}.*)'.format(second_level_tags[j])
                else:
                    second_pattern_str = '({}.*?){}'.format(second_level_tags[j], second_level_tags[j + 1])
                second_level_html = re.search(second_pattern_str, first_level_html).group(1)
                all_tags.append(second_level_html)
        # print(all_tags)
        dic = {
        }
        second_level_dic = {
            '工商信息': 'baseInfo',
            '分支机构': 'branch',
            '变更记录': 'changeInfo',
            '主要人员': 'staffCount',
            '股东信息': 'holderInfo',
        }
        for _ in all_tags:
            html = B(_, 'html.parser')
            title = html.find('h3').find('span').get_text(strip=True)
            if '工商信息' in title:
                data = self.base_parse(html)
                if data:
                    dic[second_level_dic[title]] = data
            elif title in ['分支机构','变更记录']:
                data = self.table_parse(html)
                if data:
                    dic[second_level_dic[title]] = data

    # 工商信息
    def base_parse(self, html):
        dic = {}
        lists = html.find_all('p', attrs={'class': 's10'})
        first_list = lists[0].get_text(strip=True)
        tmp = re.search('企业名称：(.*)工商注册号：(.*)统一信用代码：(.*)', first_list)
        # 公司名称
        # company_name = tmp.group(1)
        # 工商注册号
        dic['registerNum'] = tmp.group(2)
        # 统一社会信用代码
        dic['creditCode'] = tmp.group(3)
        tmp_dic = {
            '法定代表人': 'legalMan',
            '组织机构代码': 'OrganizationCode',
            '企业类型': 'companyType',
            '所属行业': 'industry',
            '经营状态': 'businessState',
            '注册资本': 'registerMoney',
            '注册时间': 'registerTime',
            '注册地址': 'registerAddress',
            '营业期限': 'businessTimeout',
            '经营范围': 'businessScope',
            '登记机关': 'registOrgan',
            '核准日期': 'confirmTime',
        }
        for _ in lists[1:]:
            try:
                key, value = _.get_text(strip=True).split('：')
                dic[tmp_dic[key]] = value
            except Exception as e:
                log.error(e)
        return dic if dic else None

    # 表格的解析
    def table_parse(self, html):
        title_dic = {
            '分支机构': ['bCompanyName', 'bTime', 'bState', 'bName'],
            '变更记录': ['changeItem', 'changeBefore', 'changeAfter', 'changeTime'],
        }

        lists = []
        tables = html.find_all('table')
        title = html.find('h3').find('span').get_text(strip=True)

        for table in tables:
            trs = table.find_all('tr')[1:]
            for tr in trs:
                dic = {}
                all_tds = tr.find_all('td')
                first_td = all_tds[0].get_text(strip=True)
                tds = all_tds[1:]
                if not first_td:
                    tmp_dic = lists.pop()
                    for _ in range(len(tds)):
                        dic[title_dic[title][_]] = tmp_dic[title_dic[title][_]] + tds[_].get_text(strip=True)
                else:
                    for _ in range(len(tds)):
                        dic[title_dic[title][_]] = tds[_].get_text(strip=True)
                    lists.append(dic)
        print(lists)



if __name__=='__main__':
    realpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/') + "/log/"
    filename = "{}_html_debug_{}.log".format(realpath, time.strftime("%Y-%m-%d", time.localtime()))

    log.basicConfig(
        level=log.DEBUG,
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

    base = HtmlAnalysis()
    base.run()