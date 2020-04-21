import os
import time
MONTH = int(time.strftime('%m',time.localtime(time.time())))
# mongo connect config
HOSTS = ['10.2.1.216:57017','10.2.1.217:57017','10.2.1.218:57017']
SOURCE = 'admin'
USERNAME = 'rwuser'
PASSWORD = '48bb67d7996f327b'

# mongo database and collection
ALL_DB = 'all_com'                                   # 名录库
# ALL_SET = 'all_results'                             # 名录表
ALL_SET = '{}_all_results'.format(MONTH)            # 名录新表
ALL_INDEX_SET = 'all_index_results'                 # 名录新表
TYC_DB = 'tyc_com'                                   # 天眼查库
NAME_SET = 'name_results'                           # 姓名表
ACCOUNT_SET = 'report_account_results'             # 天眼查账号表
ERROR_SET = 'url_error_results'                     # 访问错误url存储
MINGLU_DB = 'minglu_db'                             # 临时名录库
TMP_QCM_SET = 'tmp_qichamao_index_results'        # 临时企查猫名录库
TMP_ZY_SET = 'tmp_zhongyi_index_results'          # 临时中意名录库
TMP_SD_SET = 'tmp_shuidi_index_results'          # 临时水滴名录库

# redis connect config
DB = 13
HOST = '10.2.1.91'
R_PASSWORD = 'Dgg!@76322658'

# default log name
FILE_NAME = 'debug.log'

# txt path
IMG_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + "//"
if not os.path.exists(IMG_PATH):
    os.mkdir(IMG_PATH)



"mongodump -h 10.2.1.216:57017 -u rwuser -p 48bb67d7996f327b -d all_com  -o G:/projects/ --authenticationDatabase admin"

"mongodump -h 10.2.1.216:57017 -u rwuser -p 48bb67d7996f327b -d patent_com -c minglu -o F:/projects/ --authenticationDatabase admin"

"mongodump -h 10.2.1.216:57017 -u rwuser -p 48bb67d7996f327b -d patent_com -c old_detail_results -o F:/projects/ --authenticationDatabase admin"

"mongodump -h 10.2.1.216:57017 -u rwuser -p 48bb67d7996f327b -d patent_com  -o G:/projects/ --authenticationDatabase admin"

