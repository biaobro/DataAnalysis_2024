# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_getCouponDetail.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:00
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:00 
@Version            : 1.0
@Description        : None
"""

'''
说明：
系统路径：票券 - 票券销售设置 - 票券销售申请单管理
用的方法是：获取点击【导出】按钮后，服务器返回的文件流。
所以实现过程相对简单，只需要拿到券销售单号这1个参数就行，而不用管券销售单中有多少个券。
在旧版系统里就得用两个参数，1个券销售单号，1个券销售单包含的券数量。
直接使用导出文件，就是对方给什么就用什么，文件里只有下面这6个字段
销售申请单号，票券编号，票券状态，打印序号，有效开始时间，有效截止时间

'''

import requests
import datetime
import time
import os

from oristar import oristar_basicInfo
from general import general_utils
from general.general_basic import *


def getCouponDetail(dfCouponBatch):
    print("grab coupon detail start...")
    # 整体开始时间
    allStartTime = time.perf_counter()

    # 生成1个以当前年月日时分秒命名的文件夹,用于保存下载到的券明细
    # 每个券销售单，对应1个Excel文件
    filePath = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + '/'
    os.makedirs(os.path.dirname(filePath))

    for i in range(dfCouponBatch.shape[0]):
        # join params , get url
        url_couponDetail = "http://api.oristarcloud.com/coupon/apply/export?applyCode={}&restrict=0&exportConsume=0".format(
            dfCouponBatch.iloc[i]['applyCode'])

        # 打印拼接完成后的请求地址
        # print(url_couponDetail)

        # 单个记录（销售单）开始时间
        startTime = time.perf_counter()

        # 请求开始
        # print('row ' + str(i) + ': applyCode: ' + source_file.iloc[i]['applyCode'] + ' grab start ')

        # access the url
        try:
            response = requests.post(url_couponDetail, headers=oristar_basicInfo.headers)
        except Exception as e:
            print(e)
            return False

        # 返回头中包含Excel文件名，可以打印出来
        # print(response.headers['filename'])

        # check the result
        if response.status_code == 200:
            # len(str(totalRecord)) 判断totalRecord 是几位数
            # 比如这家影城共21个销售单，21是2位数，那输出的文件名是01,02...11,12... 不足2位数的补0
            with open(filePath + str(i).zfill(len(str(dfCouponBatch.shape[0]))) + '.xlsx', 'wb') as f:
                f.write(response.content)

            # 单个记录（销售单）结束时间
            endTime = time.perf_counter()

            # 请求结束 - 输出
            # print('row ' + str(i) + ': applyCode: ' + df.iloc[i]['applyCode'] + ' grab done within '
            #       + str(endTime - startTime) + ' seconds')
            print('grab coupon detail of {}th couponSales {} done.'.format(i+1, dfCouponBatch.iloc[i]['applyCode']))
        else:
            print("error exit" + str(response.status_code))
            print("please contact technical support.")
            return None
            # exit()

    # 合并全部文件
    dfCouponDetail = general_utils.excelFileCombine(filePath)

    # 整体结束时间
    allEndTime = time.perf_counter()
    print("grab all {} coupons within {} seconds".format(dfCouponDetail.shape[0], allEndTime - allStartTime))

    # 写入Excel
    fileName = "oristar_couponDetail_" + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + ".xlsx"

    # dfCouponDetail.to_excel(fileName, index=False)
    general_utils.excelFileGenerate(dfCouponDetail, fileName)
    # print('{} write complete.'.format(fileName))

    return dfCouponDetail


# # 登录
# oristar_login.login()
#
# # 获取券详情，需要先获取券销售单列表
# df_couponSalesList = oristar_getCouponSalesList.getCouponSalesList()
#
# # 获取券详情
# getCouponDetail(df_couponSalesList)
