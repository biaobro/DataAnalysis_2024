# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_getCrmIframeInfo.py
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

from general.general_basic import *

'''
Cookie: 
    JSESSIONID=C1E075DABC180F5637DFED5A2B780168; 
    sso_token=ddf65962-5cd7-41e0-8dbc-4b0df4b04a22; 
    _qddaz=QD.6rg6o0.bw2dfs.kycm9uub; 
    LCNUM=58c7ff33-05c1-4f09-b9db-9b944c9f0c19

说明:
    爬取路径，严重依赖对方页面组织结构。 一旦对方页面改版，代码势必需要修改。
    所以很难搞1套万年皆准的代码

'''
# 用于请求二级菜单的payLoad
payload_1st = {
    'code': cxcpm_basicInfo.menuCode_ticket
}

# 用于请求二级子菜单 ...  的payLoad
payload_2nd = {
    'targe': '',
    'sso_token': '',
    'license_number': '',
    '_': ''
}

# 用于请求正式数据 ... 的payLoad
payload_3rd = {
    'start': 0,
    'pageNum': 1,
    'limit': 15
}

# 只需要调用1次，重复调用404
def getCrmIframeInfo():
    # 第1步 请求 floatSecondMenu
    # 网站页面的标准请求用的 Cookie 值字段很多，但经过测试发现只有 CPMSESSIONID 也能请求成功，所以先按简单方式来
    # 这个页面的请求头中，'Content-Type' 和 'Referer' 有变化，所以重新赋值
    # 测试确认，'Content-Type' 必须， 'Referer' 非必须
    cxcpm_basicInfo.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    # basicInfo.headers['Referer'] = 'http://www.cxcpm.com/'

    try:
        response = requests.post(url=cxcpm_basicInfo.url_floatSecondMenu,
                                 headers=cxcpm_basicInfo.headers,
                                 data=payload_1st)
    except Exception as e:
        print(e)
        return False

    print(response)

    if response.status_code == 200:
        print("getFloatSecondMenu success")

        # response.text 是字符串 str 格式
        # print(type(response.text))
        # print(response.text)

        # response.json() 输出格式：list
        # print(type(response.json()))

        # json.dumps() 输出格式：str
        # print(type(json.dumps(response.text)))

        # json.loads() 输出格式：list
        # print(type(json.loads(response.text)))

        # 对于 【券销售单管理】 这个菜单来说，路径是固定的
        # response.text 包含3个二级菜单：票券基础设置，票券销售发行，财务管理，对应索引0，1，2
        # 【券销售单管理】是 【票券销售发行】的第1个子菜单
        # 'secondResources' 和 'url' 这种都是强依赖网站路径的，请保持高度关注
        url_1st = json.loads(response.text)[1]['secondResources'][0]['url']
        # print(url_1st)

        # 从url 中解析出我们想要的值
        url_couponApplyCodeList_dict = cxcpm_utils.url2Dict(url_1st)

        # 不知道为什么是 targe 而不是 target
        # payload_2nd['targe'] = url_couponApplyCodeList_dict.get('targe')
        # payload_2nd['sso_token'] = url_couponApplyCodeList_dict.get('sso_token')
        # payload_2nd['license_number'] = url_couponApplyCodeList_dict.get('license_number')
        # payload_2nd['_'] = str(round(time.time() * 1000))

        cxcpm_basicInfo.targe = url_couponApplyCodeList_dict.get('targe')
        cxcpm_basicInfo.sso_token = url_couponApplyCodeList_dict.get('sso_token')
        cxcpm_basicInfo.license_number = url_couponApplyCodeList_dict.get('license_number')

    else:
        print('getFloatSecondMenu failed ' + str(response.status_code))
        return

    # 第2步 请求 crm-ifram.jsp 要得到 JSESSIONID 和 LCNUM
    url_crmIframe = url_1st + '&_=' + str(round(time.time() * 1000))
    # print(url_crmIframe)

    # 调整 basicInfo.headers
    cxcpm_basicInfo.headers.pop('Content-Type')
    cxcpm_basicInfo.headers['Host'] = 'crm.cxcpm.com'  # 必须设置，否则404
    cxcpm_basicInfo.headers['Referer'] = cxcpm_basicInfo.url_host
    # 这步的请求 Cookie中只有 _qddaz
    cxcpm_basicInfo.headers['Cookie'] = "_qddaz={}".format(cxcpm_basicInfo.qddaz)

    # print(basicInfo.headers)

    # 提交请求
    try:
        response = requests.get(url=url_crmIframe, headers=cxcpm_basicInfo.headers)
    except Exception as e:
        print(e)
        return False
    print(response)

    if response.status_code == 200:
        print("getCrmIframe success")
        print(response.cookies)

        # 解析出 LCNUM,JSESSIONID,sso_token
        final_cookie = cxcpm_utils.get_cookiesValue(response.cookies) + ";_qddaz={}".format(cxcpm_basicInfo.qddaz)
        cxcpm_basicInfo.headers['Cookie'] = final_cookie
        return final_cookie
    else:
        print("getCrmIframe failed" + str(response.status_code))
        return
