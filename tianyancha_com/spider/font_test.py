import re,json
str = '{"id":1698375,"name":"阿里巴巴（中国）网络技术有限公司","type":1,"matchType":null,"base":"浙江","legalPersonName":"戴珊","estiblishTime":"1999-09-09 00:00:00.0","regCapital":"330886万美元","regStatus":"存续","score":"99","orginalScore":"9974","bonusScore":"0","companyScore":"99","historyNames":null,"categoryCode":"2100","industry":null,"humanNames":null,"trademarks":null,"tmList":null,"productList":null,"usedBondName":null,"bondName":"阿里巴巴","bondNum":"BABA","bondType":"","newtestName":null,"regNumber":null,"orgNumber":null,"creditCode":"91330100716105852F","businessScope":"开发、销售计算机网络应用软件；设计、制作、加工计算机网络产品并提供相关技术服务和咨询服务；服务：自有物业租赁，翻译，成年人的非证书劳动职业技能培训"涉及许可证的除外"。（依法须经批准的项目，经相关部门批准后方可开展经营活动）","regLocation":"浙江省杭州市滨江区网商路699号","phone":"0571-85022088\t;\t","phoneList":["0571-85022088"],"phoneNum":"0571-85022088","logo":"https://img5.tianyancha.com/logo/lll/d41d8cd98f00b204e9800998ecf8427e.png@!f_200x200","city":"杭州市","district":null,"emails":"tangxian.gongtx@alibaba-inc.com\t;\tsophy.ly@alibaba-inc.com\t;\t","emailList":["tangxian.gongtx@alibaba-inc.com","sophy.ly@alibaba-inc.com"],"websites":"www.alibaba-cneast.com\t;\twww.lwurl.to\t;\twww.aliunicorn.com\t;\twww.alibaba.org\t;\twww.alibabatech.com\t;\twww.alimails.com\t;\twww.lwurl.to\t;\twww.aliapp.co\t;\twww.alibaba.org\t;\twww.meitipu.com\t;\twww.rongzichina.com.cn\t;\twww.expo-ieia.com\t;\twaimaoquan.com\t;\twww.alibaba.org\t;\twww.alimails.com\t;...\t","hiddenPhones":null,"abbr":"阿里巴巴集团\t;\t阿里巴巴\t;\t阿里巴巴（中国）网络技术有限公司\t;\tAlibaba\t;\t阿里巴巴\t:#1#\t;\t零售通\t:#1#\t;\t阿里小蜜\t:#1#\t;\t神鲸\t:#1#\t;\t智选\t:#1#\t;\t淘宝直播\t:#1#\t;\t阿里巴巴\t:#2#\t;\t","tagList":null,"companyType":1,"companyOrgType":"有限责任公司\t港、澳、台","labelList":["高新企业"],"matchField":{"field":"项目","content":"阿里巴巴"},"latitude":30.195606649759185,"longitude":120.19862349394758,"legalPersonId":"1948885115","legalPersonType":"1","distance":null,"categoryStr":"软件和信息技术服务业","isClaimed":0,"isBranch":0,"alias":"阿里巴巴","claimInfo":null,"contantMap":null}'
# math =re.findall(r'".*?":.*?,', str)
str = str.replace('\"\"','None').replace('\'', '\"').replace('null','None').replace('true', 'True')
# res = eval(str)
# res = json.loads(str,encoding='utf-8')
# print(res)
# quit() = {}
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

data = {}
for _ in key_list:
    pattern = r'"{}":"?(.*?\"?.*?\"?.*?)"?,'.format(_)
    data[_] = re.search(pattern,str).group(1)
data['emailList'] = re.search(r'"emailList":"?(.*?\"?.*?\"?.*?)"?,"websites"',str).group(1)
data['phoneList'] = re.search(r'"phoneList":"?(.*?\"?.*?\"?.*?)"?,"phoneNum"',str).group(1)
print(data)
a = re.sub(r'"',r"'",res)
# bb = re.sub(res, a, str)
# print(bb)

# o_res = re.search(r'"name":"(.*?)",',base_txt).group(1)
# s_res = re.sub(r'"',r"'",o_res)
# base_txt = re.sub(o_res, s_res, base_txt)