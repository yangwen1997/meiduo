# Redis数据库地址
REDIS_HOST = '10.2.1.91'

#redis库
REDIS_DB = 4

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'Dgg!@76322658'

# 配置信息，无需修改
REDIS_DOMAIN = '*'
REDIS_NAME = '*'

# 若快打码相关配置
RUOKUAI_USERNAME = 'brantzxj'
RUOKUAI_PASSWORD = 'dgg123456'
RUOKUAI_SOFT_ID = '108559'
RUOKUAI_SOFT_KEY = '438362e5d4454a2c92db4ad847463b7a'
RUOKUAI_TYPE_CODE = 3040

# 产生器默认使用的浏览器
DEFAULT_BROWSER = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'sooip': 'SooipCookiesGenerator',
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'sooip': 'SooipValidTester'
}

# 产生器和验证器循环周期
GEN_CYCLE = 100
VALID_CYCLE = 3600

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5500

# 进程开关
# 产生器，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = False
# API接口服务
API_PROCESS = False

