# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_getCinemaInfo.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:03 
@Version            : 1.0
@Description        : None
"""

import requests
import time
from cxcpm import cxcpm_basicInfo
from cxcpm import cxcpm_utils

from general.general_basic import *


def getCinemaInfo():
    # set the specified header
    cxcpm_basicInfo.headers['Host'] = 'www.cxcpm.com'
    cxcpm_basicInfo.headers['Referer'] = 'http://www.cxcpm.com/users/login'
    cxcpm_basicInfo.headers['Content-Type'] = 'application/json;charset=UTF-8'
    cxcpm_basicInfo.headers['Cookie'] = cxcpm_utils.get_cookiesValue(cxcpm_basicInfo.cookies_loginSuccess)

    try:
        response = requests.post(url=cxcpm_basicInfo.url_cinemaInfo,
                                 headers=cxcpm_basicInfo.headers,
                                 cookies=cxcpm_basicInfo.cookies_loginSuccess)
    except Exception as e:
        print(e)
        return False

    if response.status_code == 200:
        print("get cinemaInfo success")

        # 返回信息中包含 影城名称 ID  影城8位专资编码
        # tenantLicense cinemaUid 看起来像是慧影云编码
        # createTime 13位的Unix 时间  可以认为是系统开通时间
        # tenantId=425024 是从这里得到？
        # print(response.text)

        # 得到8位编码
        cxcpm_basicInfo.cinemaCode = response.json()['code']
        print("cinema code : {}".format(cxcpm_basicInfo.cinemaCode))

        # 得到影城名称
        cxcpm_basicInfo.cinemaName = response.json()['name']
        print("cinema name : {}".format(cxcpm_basicInfo.cinemaName))

        # 得到系统开通时间
        # creatTime 是13位毫秒时间戳
        # python 默认是10位秒时间戳
        cxcpm_basicInfo.cinemaSystemInitTime = time.strftime("%Y-%m-%d %H:%M:%S",
                                                             time.localtime(response.json()['createTime']/1000))
        print("cinema system init time : {}".format(cxcpm_basicInfo.cinemaSystemInitTime))
    else:
        print('get cinemaInfo failed, please contact technical support.')
        return


# cxcpm_login.login()
# getCinemaInfo()