# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_getCoupon.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 22:59
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 22:59 
@Version            : 1.0
@Description        : None
"""

from oristar import oristar_getCouponDetail, oristar_getCouponSalesList, oristar_getCinemaInfo
from general.general_basic import *
from general.general_dataStandardize import dataStandardize


# 输出券销售单列表 和 券明细
def getCoupon():
    oristar_getCinemaInfo.getCinemaInfo()

    # dfCouponBatch, dfCouponDetail
    # 获取券详情，需要先获取券销售单列表
    dfCouponBatch = oristar_getCouponSalesList.getCouponSalesList()

    # 获取券详情
    dfCouponDetail = oristar_getCouponDetail.getCouponDetail(dfCouponBatch)

    # 文件转换
    dataStandardize(dfCouponBatch, dfCouponDetail, 'oristar')

    print('oristar coupon data grab done. please check the file in current folder.')
