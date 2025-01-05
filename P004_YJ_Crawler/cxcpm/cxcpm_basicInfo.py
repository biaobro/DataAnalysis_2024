# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_basicInfo.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:03 
@Version            : 1.0
@Description        : None
"""

# from fake_useragent import UserAgent
from requests.cookies import RequestsCookieJar

# 影城信息
cinemaCode = ''
cinemaName = ''
cinemaSystemInitTime = ''

# 各个页面的url, 统一用主页为参考
host = "www.cxcpm.com"
url_host = "http://www.cxcpm.com"
url_login = url_host + "/users/login"
url_cinemaInfo = url_host + '/switchCinema/setDefaultCinema'

url_floatSecondMenu = url_host + '/floatSecondMenu'
url_couponApplyCodeList = url_host + '/crm/couponApplyQueryAction.do?method=page'

# 2147483647 在i.js 的好几处函数中用到，所以抽出来统一定义，便于统一调整
random_seed = 2147483647

# Cookie 用到
qddaz = ''
targe = ''
sso_token = ''
license_number = ''

# 定义1个变量，用于保存登录成功后得到的 Cookie -> CPMSESSIONID
cookies_loginPage = RequestsCookieJar()
cookies_loginSuccess = RequestsCookieJar()


loginStatus = False

# 用户输入的登录信息
loginPayLoad = {
    'customerCode': '',
    'loginName': '',
    'loginType': 'customerCode',
    'password': ''
}

# 登录信息 usable
loginPayLoadUsable = {
    'customerCode': '4c9dd9af49927974',
    'loginName': 'zc808946',
    'loginType': 'customerCode',
    'password': 'zc1234'
}

# 登录页面的请求 没有Cookie
'''
Content-Type : 
    application/json : 需要用json.dumps(payload) 将字典转换为Json
    application/x-www-form-urlencoded : 直接提交payload
    所以这个Content-Type也很重要，决定了不同payload的编码方式
    为了尽量保持通用，这里的header可以先保留为空，然后在每个业务请求里再去赋值
    其他字段也是同理
'''
headers = {

    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '',
    'Host': 'www.cxcpm.com',
    'Origin': 'http://www.cxcpm.com',
    'Referer': url_login,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    # 'User-Agent': UserAgent().random,
    'X-Requested-With': 'XMLHttpRequest',
}

# 一级菜单编码
menuCode_member = 'orst##cmc_member'  # 会员
menuCode_ticket = 'orst##cmc_ticket'  # 票券
