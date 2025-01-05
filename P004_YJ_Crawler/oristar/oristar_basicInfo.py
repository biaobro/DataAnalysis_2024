# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_basicInfo.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2022/6/21 15:42
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2022/6/21 15:42
@Version            : 1.0
@Description        : None
"""

# 每个页面/请求 对应的接口/网址不同
# 登录页面
url_base = "http://api.oristarcloud.com"
url_login = url_base + "/cpm/user/login"
url_couponSalesList = url_base + "/coupon/apply/query"
url_cinemaInfo = url_base + "/cpm/user/auth/listDataPurviews"


# 影城信息
cinemaCode = ''
cinemaName = ''
cinemaSystemInitTime = ''


# 需要有个变量保存登录状态？ 作为其他操作的参照
loginStatus = False


# 用户信息
# 注意这里的定义，单词必须小写 否则报"服务端错误"（包括大小写）
loginPayLoad = {
    "customerCode": "",
    "loginName": "",
    "password": "",
    "showSlider": True
}

# 至潮印象城店信息 测试可用 loginPayLoadUsable
loginPayLoadUsable = {
    "customerCode": "xcwdc",
    "loginName": "001",
    "password": "123456a",
    "showSlider": True
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://www.oristarcloud.com',
    'Host': 'api.oristarcloud.com',
    'Referer': 'http://www.oristarcloud.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Cpm-User-Key': '',
    'Cpm-User-Token': ''
}
