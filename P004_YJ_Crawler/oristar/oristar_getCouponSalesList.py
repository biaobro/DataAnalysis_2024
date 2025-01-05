# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_getCouponSalesList.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:00
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:00 
@Version            : 1.0
@Description        : None
"""

'''
# 说明：用以获取券销售单列表
# 日期： 20220104
'''

import pandas as pd
import requests
import math
import datetime
import time
import json

from oristar import oristar_basicInfo
from general.general_basic import *
from general import general_utils

# 这个页面的payLoad 字段不一致，所以单独写
# pageSize:网页上标准请求用的值是10。这家影城因为目测仅21条，所以其实可以直接使用21. 测试也没有问题
# 不过按照标准10处理，肯定是没有问题的
# 如果确实数量大，可以先按10条请求1次，在返回信息中会包含总记录数pageNum，然后分批次请求即可
couponSalesListPayLoad = {
    "applyCode": '',
    "auditState": '',
    "contractCode": '',
    "couponName": '',
    "couponType": '',
    "state": '',
    "queryCreateUserName": '',
    "auditName": [],
    "createTimeStart": '',
    "createTimeEnd": '',
    "validDateStart": '',
    "validDateEnd": '',
    "custId": '',
    "incomeCinemaId": '',
    "pageSize": 10,  # 21
    "pageNo": 1
}


def getCouponSalesList():
    # access the url
    # 先请求1次 得到pageNum
    # 注意是post 方式
    try:
        response = requests.post(oristar_basicInfo.url_couponSalesList,
                                 headers=oristar_basicInfo.headers,
                                 data=json.dumps(couponSalesListPayLoad))
    except Exception as e:
        print(e)
        return False

    totalRecordCount = json.loads(response.text)['pageNum']
    print("there are {} coupon sales records.".format(totalRecordCount))
    # print(math.ceil(totalRecordCount / 10))

    # 整体开始时间
    allStartTime = time.perf_counter()

    # 创建1个空的 DataFrame
    dfCouponBatch = pd.DataFrame()

    # 循环取全部页面
    # math.ceil(21/10) = 3  ceil 向上取整 如果是21条，那需要循环3次
    for i in range(math.ceil(totalRecordCount / 10)):

        # 提供页编码 从1开始
        couponSalesListPayLoad['pageNo'] = i + 1

        # 提交请求
        response = requests.post(oristar_basicInfo.url_couponSalesList,
                                 headers=oristar_basicInfo.headers,
                                 data=json.dumps(couponSalesListPayLoad))

        # print(json.loads(response.text))

        # json.loads(response.text['data']) 和 response.json()['data'] 得到的数据格式不同
        # check the result
        if response.status_code == 200:
            print('grab couponSalesList in pageNum {} done'.format(couponSalesListPayLoad['pageNo']))
            # 测试格式
            # print(type(json_list_data))  -- 格式为 list
            # print(type(json.loads(response.text)))  -- 格式为 dict
            # 关于生成文件的类型，csv 更轻便
            # csv 是直接记录文本的，但如果用Excel打开csv，有些数字会被转成科学计数法，而且无法转成文本
            # 第1种解决方法，不直接打开，而是Excel - 数据 - 从文本/csv 加载，这样可以保持数据原貌
            # 第2种解决方法，直接写成Excel 的 xlsx 格式

            # 直接写成 Excel xlsx 格式
            # pandas 可以直接读取dict 格式
            # append 追加数据
            dfCouponBatch = dfCouponBatch.append(pd.DataFrame(json.loads(response.text)['data']))

        else:
            print("error exit." + str(response.status_code))
            print("please contact technical support.")
            return
            # exit()

    # 整体结束时间
    allEndTime = time.perf_counter()
    print("couponBatch {} records grab done within {} seconds.".format(totalRecordCount, allEndTime - allStartTime))

    # 将 dataframe 保存成 excel
    # 文件命名为 当前年月日时分秒
    fileName = 'oristar_couponBatch_' + datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S') + '.xlsx'
    # dfCouponBatch.to_excel(fileName, index=False)
    general_utils.excelFileGenerate(dfCouponBatch, fileName)
    print('{} write complete'.format(fileName))

    # 将数据返回，供后续使用
    return dfCouponBatch

# oristar_login.login()
# getCouponSalesList()
