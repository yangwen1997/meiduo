# import gevent
# from gevent import monkey
# monkey.patch_all()
import os, time, sys
from common import get_proxy, logger
# from spider.fixed_normal_account_company_spider import NormalAccountCompanySpider
# from spider.second_program_company_spider import CompanySpider
from new_check_account_company_spider import CompanySpider
# from spider.dy_normal_account_company_spider import NormalAccountCompanySpider
# from spider.keywords_limit_condition_spider import KeywordLimitConditionSpider

def run(proxy_tag, num):
    proxy_list = get_proxy(proxy_tag, log)  # 获取静态IP
    # quit()
    # proxy_list = [{'ip': '36.59.220.63:22404', 'mac': '414162ee-720d-4458-9388-e78b9a9890e4'}]  # 获取静态IP
    
    tasks = []
    count = num
    "0 5 10 15"
    main(proxy_list[num], count, proxy_tag)
    # for _ in proxy_list[:10]:
    #     tasks.append(gevent.spawn(main, _, count, proxy_tag))
    #     gevent.sleep(1)
    #     count += 1
    # gevent.joinall([*tasks])


def main(proxy, count, proxy_tag):
    C = CompanySpider(img_path, count, proxy, proxy_tag, log)
    C.run()
    # N = NormalAccountCompanySpider(img_path, proxy, count, proxy_tag)
    # N = KeywordLimitConditionSpider(img_path, proxy, count, proxy_tag)
    # N.run(log)



if __name__ == '__main__':
    '''日志配置'''
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + "/log/"
    img_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + "/img/"
    # print(img_path)
    # from PIL import Image, ImageFont, ImageDraw
    # image_info = Image.open('{}img_normal{}.png'.format(img_path, str(2)))
    # print(image_info)
    # quit()
    # if not os.path.exists(real_path):
    #     os.mkdir(real_path)

    '''-------'''
    # a = redis_data()
    # proxy_tag-> 1:表示用vps_static_ip_results静态IP, 2:表示使用香港的静态IP
    # try:
    #     proxy_tag = int(sys.argv[1])
    # except Exception:
    #     proxy_tag = 1
    proxy_tag = 1
    try:
        num = int(sys.argv[1])
    except Exception:
        num = 0
    file_name = "{}search_company_{}_{}.log".format(real_path,num,
                                                 time.strftime("%Y-%m-%d",
                                                               time.localtime()))
    log = logger(file_name)

    run(proxy_tag, num)








