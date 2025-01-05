# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_getCouponSalesList.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:02
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:02 
@Version            : 1.0
@Description        : None
"""

import requests
import pandas as pd
import datetime
from cxcpm import cxcpm_getCrmIframeInfo, cxcpm_basicInfo
from general.general_basic import *
from general import general_utils

# 用于请求正式数据 ... 的payLoad
payload_3rd = {
    'start': 0,
    'pageNum': 1,
    'limit': 15
}


def getCouponSalesList():
    # 第3步： 请求正式数据
    url_couponApplyCodeList = 'http://crm.cxcpm.com/crm/couponApplyQueryAction.do?method=page'

    cxcpm_basicInfo.headers['Referer'] = url_couponApplyCodeList
    cxcpm_basicInfo.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    # final_cookie = cxcpm_getCrmIframeInfo.getCrmIframeInfo() + ";_qddaz={}".format(cxcpm_basicInfo.qddaz)
    # cxcpm_basicInfo.headers['Cookie'] = final_cookie

    # print(cxcpm_basicInfo.headers)

    # 提交正式数据请求 这里用的是 post
    try:
        response = requests.post(url=url_couponApplyCodeList, headers=cxcpm_basicInfo.headers, data=payload_3rd)
    except Exception as e:
        print(e)
        return False
    print(response)

    if response.status_code == 200:
        print("getCouponSalesList success")
        # print(response.text)
        # print(type(response.text))

        # 得到总记录条数
        print("There are total {} coupon sales records ".format(str(response.json()['totalCount'])))

    else:
        print("getCouponSalesList error" + str(response.status_code))
        return

    # 第4步 处理数据 保存成文件
    # 第1次正式请求的返回结果中，会包含 totalCount， 标准处理的话就是循环 totalCount/pageNum 次
    # 创建1个空的 DataFrame
    dfCouponBatch = pd.DataFrame()

    # range 是左闭右开
    for page in range(int(response.json()['totalCount']) // payload_3rd['limit'] + 1):
        payload_3rd['start'] = payload_3rd['limit'] * page
        payload_3rd['pageNum'] = page + 1

        # 发送请求
        try:
            response = requests.post(url_couponApplyCodeList, headers=cxcpm_basicInfo.headers, data=payload_3rd)
        except Exception as e:
            # 异常处理：其实可以改为重试N次，如果全部失败，再退出
            print(e)
            return False

        # check the result
        if response.status_code == 200:
            print('grab couponSalesList in pageNum {} done'.format(payload_3rd['pageNum']))
            # response.json()['result'] 是 list
            # list 可以直接转 DataFrame
            dfCouponBatch = dfCouponBatch.append(pd.DataFrame(response.json()['result']))

            # 页面间延迟
            # time.sleep(1)

        else:
            print('error exit' + str(response.status_code))
            return

    # 将 dataframe 保存成 excel
    # 文件命名为 当前年月日时分秒
    fileName = 'cxcpm_couponSalesList_' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + '.xlsx'
    # dfCouponBatch.to_excel(fileName, index=False)

    general_utils.excelFileGenerate(dfCouponBatch, fileName)
    print('{} write complete'.format(fileName))

    # 返回 dataframe
    return dfCouponBatch

