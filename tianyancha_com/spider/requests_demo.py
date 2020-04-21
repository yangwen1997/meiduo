#-*- coding:UTF-8 -*-
import requests,re
from common import redis_conn
from bs4 import BeautifulSoup as B


url = "https://www.tianyancha.com/search?key=%E5%BA%B7%E4%B8%96%E4%BF%AD"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cookie': 'ssuid=7703879792; TYCID=8971320038af11e99421a35550a0a6c7; undefined=8971320038af11e99421a35550a0a6c7; _ga=GA1.2.210168479.1551066219; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E9%2583%25AD%25E8%2594%25B7%25E8%2596%2587%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%2522129%2522%252C%2522onum%2522%253A%252240%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTg0NDUwMTE0MiIsImlhdCI6MTU1MTA2NjI0MiwiZXhwIjoxNTY2NjE4MjQyfQ.6BJfIf_rAdYIwkneCRXeic9ZtL7xY4mGErRIZo_vCWhqC6k8-POwOQn95M24lAnY6CrFZE2NIwmNtOglyR5_zA%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215844501142%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTg0NDUwMTE0MiIsImlhdCI6MTU1MTA2NjI0MiwiZXhwIjoxNTY2NjE4MjQyfQ.6BJfIf_rAdYIwkneCRXeic9ZtL7xY4mGErRIZo_vCWhqC6k8-POwOQn95M24lAnY6CrFZE2NIwmNtOglyR5_zA; __insp_ss=1551075666199; aliyungf_tc=AQAAAIRlRSq+mAQAQBSWtu0EKZQZqkeP; csrfToken=HKgW16znHhTzPMQsyL4_cSYd; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1551066219,1551403276,1551659277; refresh_page=null; bannerFlag=true; _gid=GA1.2.838233971.1551920883; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1551947451; __insp_wid=677961980; __insp_slim=1551947452884; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vc2VhcmNoP2tleT0lRTUlQkElQjclRTQlQjglOTYlRTQlQkYlQUQ%3D; __insp_targlpt=5bq35LiW5L_tX_ebuOWFs_aQnOe0oue7k_aenC3lpKnnnLzmn6U%3D; __insp_norec_sess=true; __insp_slim=1551920897962',
    'Host': 'www.tianyancha.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
s = requests.session()
res = s.get(url,headers=headers)
html = B(res.text, 'html.parser')
spans = html.find_all('span',class_='tt hidden')
key_list = [
        'phoneList',
        'emailList',
        'id',
        'name',
        'regStatus',
        'base',
        'regCapital',
        'estiblishTime',
        'creditCode',
        'regLocation',
        'businessScope',
        'categoryStr',
        'city',
        'district',
    ]
def not_empty(s):
    return s.strip()

for _ in spans:
    res = _.get_text()
    res = res.replace('\"\"', 'None').replace('\'', '\"').replace('null',
                                                                  'None').replace(
        'true', 'True')
    data = {}

    # res = re.sub('\\t', "", res, re.U)
    # print(res.replace("\\t",''))
    for _ in key_list:
        pattern = r'"{}":"?(.*?\"?.*?\"?.*?)"?,'.format(_)
        data[_] = re.search(pattern, res).group(1)
    em_list = re.search(r'"emails":"?(.*?\"?.*?\"?.*?)"?,"emailList"', res).group(1).replace("\\t",'').split(';')
    # filter(None, em_list)
    em_list = [x for x in em_list if x != '' and x != 'None']
    data['emailList'] = em_list if em_list else ''
    # data['emailList'] = re.sub('\s+', "", data['emailList'],re.I)
    ph_list = re.search(r'"phone":"?(.*?\"?.*?\"?.*?)"?,"phoneList"', res).group(1).replace("\\t",'').split(';')
    ph_list = [x for x in ph_list if x != '' and x != 'None']
    data['phoneList'] = ph_list if ph_list else ''
    # filter(None, data['phoneList'])
    # data['phoneList'] = re.sub('\s+', "", data['phoneList'],re.I).split(';')
    print(data)
    print('---------\n')

    # print(res)
