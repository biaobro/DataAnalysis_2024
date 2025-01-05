# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_getCouponDetail.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:02
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:02 
@Version            : 1.0
@Description        : None
"""

import requests
import datetime
import os
import time
import pandas as pd

from cxcpm import cxcpm_basicInfo
from cxcpm import cxcpm_login
from cxcpm import cxcpm_getCouponSalesList

from general import general_utils
from general.general_basic import *


def getCouponDetail(dfCouponBatch):
    # 整体开始时间
    allStartTime = time.perf_counter()

    # 旧版券销售单实际也提供了导出券功能
    # 生成1个以当前年月日时分秒命名的文件夹,用于保存下载到的券明细
    # 每个券销售单，对应1个Excel文件
    filePath = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + '/'
    os.makedirs(os.path.dirname(filePath))

    for i in range(dfCouponBatch.shape[0]):

        # join params , get url
        url_couponApply = "http://crm.cxcpm.com/crm/couponapplyAction.do?method=exportTicketNum&applyCode={}".format(
            dfCouponBatch.iloc[i]['applyCode'])

        # 打印拼接完成后的请求地址
        # print(url_couponApply)

        # 单个记录（销售单）开始时间
        startTime = time.perf_counter()

        # 请求开始
        # print('row ' + str(i) + ': applyCode: ' + source_file.iloc[i]['applyCode'] + ' grab start ')

        # access the url
        # 旧版的下载用的请求方式 又是 get, 真TM乱
        try:
            response = requests.get(url_couponApply, headers=cxcpm_basicInfo.headers)
        except Exception as e:
            print(e)
            return False

        # 返回头中包含Excel文件名，可以打印出来
        # print(response.headers['filename'])

        # check the result
        if response.status_code == 200:
            # len(str(totalRecord)) 判断totalRecord 是几位数
            # 比如这家影城共21个销售单，21是2位数，那输出的文件名是01,02...11,12... 不足2位数的补0
            # @20220121 这种通过【下载】方式得到的文件，缺少 有效起始/截止 时间字段，需要从券批次文件中补回来
            with open(filePath + str(i).zfill(len(str(dfCouponBatch.shape[0]))) + '.xlsx', 'wb') as f:
                f.write(response.content)

            # 单个记录（销售单）结束时间
            endTime = time.perf_counter()

            # 请求结束 - 输出
            # print('row ' + str(i) + ': applyCode: ' + df.iloc[i]['applyCode'] + ' grab done within '
            #       + str(endTime - startTime) + ' seconds')
            print('grab {}th couponSales {} done.'.format(i + 1, dfCouponBatch.iloc[i]['applyCode']))
        else:
            print("error exit" + str(response.status_code))
            return

    # 合并全部文件
    dfCouponDetail = general_utils.excelFileCombine(filePath)

    # 整体结束时间
    allEndTime = time.perf_counter()
    print("grab all {} coupons within {} seconds".format(dfCouponDetail.shape[0], allEndTime - allStartTime))

    # inner join detail & batch
    dfCouponDetailFinal = pd.merge(dfCouponDetail, dfCouponBatch[['applyCode', 'validDateStart', 'validDateEnd']],
                                   how='inner', left_on='销售单号', right_on='applyCode')
    print('join batch to get validDate for cxcpm coupon detail complete.')

    # 写入Excel
    fileName = "cxcpm_couponDetail_" + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + ".xlsx"

    # dfCouponDetailFinal.to_excel(fileName, index=False)
    # 不再直接調用 to_excel
    general_utils.excelFileGenerate(dfCouponDetailFinal, fileName)
    # print('{} write complete.'.format(fileName))

    return dfCouponDetailFinal

# 登录
# cxcpm_login.login()
#
# # 得到券销售单列表
# df_couponApplyCodeList = cxcpm_getCouponSalesList.getCouponSalesList()
#
# # 通过券销售单列表，进一步得到券明细
# getCouponDetail(df_couponApplyCodeList)

