# 1. 天眼查爬虫

### 文件目录
```tianyancha_com
tianyancha_com
|   __init__.py
|   account_to_redis.py     //账号写入redis
|   new_check_account_company_spider.py     // 出现验证码的账号打码操作
|   clear_chrome_cache.py   // 清理chrome缓存类
|   names_to_redis.py   // 姓名名录写入redis
|   redisdb.py      // 封装的redis类
|   rk_python3.py   // 汉字点选验证码接口类
|   slide_recognition.py    // 滑块验证码破解类
|   common.py   // 公共方法
│   config.py   // 配置文件
│   main.py     // 主程序
│   tianyancha_run0-10.bat // window下批量启动
│
└───spider // 爬虫文件
│   │   __init__.py
│   └───second_program_company_spider.py // 天眼查爬虫
|
└───log //日志文件
|
|____new_check_account_company_spider.py // 进行账号验证码验证

```
---
# 2. 域名备案爬虫

### 文件目录
```beian_com
beian_com
|   __init__.py
|   ip_to_redis.py     // ip写入redis
|   company_to_redis.py   // 公司名录写入redis
|   redisdb.py      // 封装的redis类
|   common.py   // 公共方法
│   config.py   // 配置文件
│   main.py     // 主程序
│
└───spider // 爬虫文件
│   │   __init__.py
│   │   domain_spider.py // 域名备案信息爬虫
|   └───demo.py
|
└───log //日志文件
```
---
# 3. 专利爬虫

