# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_login.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:02
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:02 
@Version            : 1.0
@Description        : None
"""

import requests
import json
import time
from cxcpm import cxcpm_basicInfo, cxcpm_utils
from cxcpm.cxcpm_utils import get_cookiesValue

from general.general_basic import *
from general.general_thread import *


def login():
    # access the login page to get first cookie
    try:
        response = requests.get(url=cxcpm_basicInfo.url_login, headers=cxcpm_basicInfo.headers)
    except Exception as e:
        print(e)
        return False

    if response.status_code == 200:

        # requests 从response 中得到的 cookies 类型是 CookieJar
        cxcpm_basicInfo.cookies_loginPage = response.cookies
        # print(type(cookies_loginPage))
        print("get cookie from login page : ")
        print(cxcpm_basicInfo.cookies_loginPage)

        # print(utils.get_cookiesValue(response.cookies))
    else:
        # open login page failed, should be network issues
        print('login page request failed, please check your network.')
        print(response)
        return
        # exit()

    print("login payload has been submitted ... please wait about 15 seconds... ")

    # submit login payload with cookie in new request
    # 这个请求提交后,即点击登录按钮后，要等10s左右，才会有新的返回
    # 网页也是同样的表现，这点需要考虑，等返回之后再执行后续
    # 目前就是死等。是否单独开1个线程 然后while 循环等待状态变更
    try:
        response = requests.post(url=cxcpm_basicInfo.url_login,
                                 headers=cxcpm_basicInfo.headers,
                                 cookies=cxcpm_basicInfo.cookies_loginPage,
                                 data=json.dumps(cxcpm_basicInfo.loginPayLoad))
    except Exception as e:
        print(e)
        return False

    if response.status_code == 200:
        if len(response.text) != 0:
            cxcpm_basicInfo.loginStatus = True
            # requests 从response 中得到的 cookies 类型是 CookieJar
            cxcpm_basicInfo.cookies_loginSuccess = response.cookies
            print("login success. get new cookie from home page : ")
            print(cxcpm_basicInfo.cookies_loginSuccess)

            # 更新header 中的Cookie
            # 因为后续的请求都是使用这里得到的CPMSESSIONID，所以直接在本文件中做替换，不再在业务处理中替换
            cxcpm_basicInfo.headers['Cookie'] = cxcpm_utils.get_cookiesValue(cxcpm_basicInfo.cookies_loginSuccess)
        else:
            # 用户名错误 && 密码错误 && 客户序列号不存在，不同错误返回的信息内容不同，没有code 没有msg
            # 所以直接打出返回内容
            print(response.text)
    else:
        # status_code = 415 header 有问题
        # status_code = 500 请求体有问题
        print(response)
        print('login failed. status code : {}'.format(response.status_code))
        return

    # 模拟交互第1步，得到 window.location.href
    locationHref = cxcpm_utils.get_locationHref()

    # 是否有必要更新Referer
    # basicInfo.headers['Referer'] = locationHref

    # 得到 tencentSig
    tencentSig = cxcpm_utils.get_tencentSig()

    # 得到pgv_pvi
    pgv_pvi = cxcpm_utils.get_randomByTime()

    # 得到 _qddaz
    cxcpm_basicInfo.qddaz = cxcpm_utils.get_qddaz(cxcpm_basicInfo.headers['User-Agent'],
                                                  pgv_pvi,
                                                  tencentSig,
                                                  cxcpm_basicInfo.url_login,
                                                  locationHref)

    print('local cookies generate done. please keep going.')

# 如果单纯测试登录的话，是否再加上logout，因为不确定是否频繁登录被拦截
# login()
