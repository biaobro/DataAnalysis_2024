# -*- coding: utf-8 -*-
'''
@20220120
1,将爬到的慧影云数据，标准化为云智导入时要求的格式

注意事项
1,考虑到字段对应关系，这里是非常僵化的代码。本地文件可固化字段位置，但抓下来的文件不能保证字段顺序和名称。
2,从效率出发，直观上将数据全部抓到本地再筛选字段是更合理的方式，而不是先筛选字段再保存。
 这样，就会有个严重的问题，新版和旧版 抓下来的数据字段命名不同。 而我们希望用尽量精简的代码完成功能

'''

import pandas as pd
from general.general_utils import *
from cxcpm import cxcpm_basicInfo
from oristar import oristar_basicInfo

localCouponBatchColumns = ['本地券码批次号(单元格格式为文本)',
                           '原使用政策描述(单元格格式为文本)',
                           '原兑换政策描述(单元格格式为文本)',
                           '流向(单元格格式为文本，长度不超过20位)',
                           '批次开始时间(YYYY-MM-DD)(单元格格式为文本)',
                           '批次结束时间(YYYY-MM-DD)(单元格格式为文本)',
                           '券模板编码(单元格格式为文本)'
                           ]

localCouponDetailColumns = ['本地券码批次号(单元格格式为文本)',
                            '券码/条形码(单元格格式为文本)',
                            '基础价格(单位分)',
                            '发行日期(YYYY-MM-DD)(单元格格式为文本)',
                            '结束时间(YYYY-MM-DD)(单元格格式为文本)',
                            '卡号(单元格格式为文本,可空)',
                            '券码状态(单元格格式为文本,可空)'
                            ]


def couponBatchStandardize(dfSrcCouponBatch, version):
    """

    :param version: oristar or cxcpm, the field name/order/data type in source file is different
    :param dfSrcCouponBatch:  coupon batch dataframe source from HYY website
    :return : dataframe target for YZ
    """
    dfTarCouponBatch = pd.DataFrame()
    # 券批次  在 oristar 上叫 batchCode， 在 cxcpm 上叫 batchNum
    # 销售单号 和 批次 就是差了 XS
    dfTarCouponBatch[localCouponBatchColumns[0]] = dfSrcCouponBatch['batchCode'].str[-16:] if version == 'oristar' else \
    dfSrcCouponBatch['applyCode'].str[-16:]

    # 券名称 在 oristar 上叫 couponName， 在 cxcpm 上叫 ticketNum
    dfTarCouponBatch[localCouponBatchColumns[1]] = dfSrcCouponBatch['couponName'] if version == 'oristar' else \
    dfSrcCouponBatch['ticketName']

    # 券兑换政策 —— 固定？
    dfTarCouponBatch[localCouponBatchColumns[2]] = '兑换券'

    # 券流向 新版旧版都叫 custName
    dfTarCouponBatch[localCouponBatchColumns[3]] = dfSrcCouponBatch['custName']

    # 券生效起始截止日期，在 oristar 上带时分秒，在 cxcpm 上只有年月日
    dfTarCouponBatch[localCouponBatchColumns[4]] = dfSrcCouponBatch['validDateStart'].str[
                                                    0:11] if version == 'oristar' else dfSrcCouponBatch[
        'validDateStart']
    dfTarCouponBatch[localCouponBatchColumns[5]] = dfSrcCouponBatch['validDateEnd'].str[
                                                    0:11] if version == 'oristar' else dfSrcCouponBatch['validDateEnd']

    # 券模板编码：导入前实施确认？
    dfTarCouponBatch[localCouponBatchColumns[6]] = ''
    # print(tarCouponBatch.info())
    print(version + ' coupon batch data localize done.')

    return dfTarCouponBatch


def couponDetailStandardize(dfSrcCouponDetail, version):
    """

    :param version:
    :param dfSrcCouponDetail:  coupon detail dataframe source from HYY website
    :return : dataframe target for YZ
    """
    dfTarCouponDetail = pd.DataFrame()

    # 只保留券状态为 已消费,已激活 的
    dfSrcCouponDetail = dfSrcCouponDetail.query('票券状态 in ["已消费","已激活"]')

    # dfSrcCouponDetail = dfSrcCouponDetail.loc[(dfSrcCouponDetail['票券状态'] == '已消费') | (dfSrcCouponDetail['票券状态'] == '已激活')]

    # print out all columns
    # print('columns in srec file:' + dfSrcCouponDetail.columns)

    # 销售申请单号 在 oristar 上是24位，只取后16位，在 cxcpm 上是 14位，字段名称也不同
    dfTarCouponDetail[localCouponDetailColumns[0]] = dfSrcCouponDetail["销售申请单号"].str[-16:] if version == 'oristar' else \
    dfSrcCouponDetail["销售单号"].str[-16:]
    dfTarCouponDetail[localCouponDetailColumns[1]] = dfSrcCouponDetail['票券编号']
    dfTarCouponDetail[localCouponDetailColumns[2]] = '0'

    # 旧版 cxcpm 导出的券详情中没有有效时间字段，是合并后的
    dfTarCouponDetail[localCouponDetailColumns[3]] = dfSrcCouponDetail['有效开始时间'] if version == 'oristar' else \
    dfSrcCouponDetail["validDateStart"]
    dfTarCouponDetail[localCouponDetailColumns[4]] = dfSrcCouponDetail['有效截止时间'] if version == 'oristar' else \
    dfSrcCouponDetail["validDateEnd"]
    dfTarCouponDetail[localCouponDetailColumns[5]] = ''

    # 券状态 已消费,已激活,已退货,已过期,已作废
    dfTarCouponDetail[localCouponDetailColumns[6]] = dfSrcCouponDetail['票券状态'].apply(
        lambda x: 'unredeemed' if x == '已激活' else 'redeemed')
    print(version + ' coupon detail data localize done.')
    return dfTarCouponDetail


def dataStandardize(dfCouponBatch, dfCouponDetail, version):
    if version == 'oristar':
        excelFileGenerate(couponBatchStandardize(dfCouponBatch, version), "{}_{}_本地券批次模板.xlsx".format(version,oristar_basicInfo.cinemaCode))
        excelFileGenerate(couponDetailStandardize(dfCouponDetail, version), "{}_{}_本地券模板.xlsx".format(version,oristar_basicInfo.cinemaCode))
    elif version == 'cxcpm':
        excelFileGenerate(couponBatchStandardize(dfCouponBatch, version), "{}_{}_本地券批次模板.xlsx".format(version,cxcpm_basicInfo.cinemaCode))
        excelFileGenerate(couponDetailStandardize(dfCouponDetail, version), "{}_{}_本地券模板.xlsx".format(version,cxcpm_basicInfo.cinemaCode))
    else:
        print("the specified version does not exist. please contact technical support. ")


# local test
# srcCouponBatch = pd.read_excel('D:\Study\crawler_hyy\cxcpm_couponSalesList_20220121153445.xlsx', dtype=str)
# srcCouponDetail = pd.read_excel('D:\Study\crawler_hyy\cxcpm_couponDetail_20220121153608.xlsx', dtype=str)
# dataStandardize(srcCouponBatch, srcCouponDetail, 'cxcpm')
