# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_getCoupon.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:03 
@Version            : 1.0
@Description        : None
"""

from cxcpm import cxcpm_getCouponDetail, cxcpm_getCouponSalesList, cxcpm_getCrmIframeInfo, cxcpm_getCinemaInfo, cxcpm_basicInfo
from general.general_basic import *
from general.general_dataStandardize import dataStandardize


def getCoupon():
    # 获取影城信息 用于最终文件命名
    cxcpm_getCinemaInfo.getCinemaInfo()

    cxcpm_getCrmIframeInfo.getCrmIframeInfo()

    # dfCouponBatch, dfCouponDetail
    dfCouponBatch = cxcpm_getCouponSalesList.getCouponSalesList()

    dfCouponDetail = cxcpm_getCouponDetail.getCouponDetail(dfCouponBatch)

    dataStandardize(dfCouponBatch, dfCouponDetail, 'cxcpm')

    print('cxcpm coupon data grab done. please check the file in current folder.')

