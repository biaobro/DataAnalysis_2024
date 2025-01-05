# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 11_excel split with pandas.py
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:06
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:06 
@Version            : 1.0
@Description        : None
"""
import datetime

# 文件名，要注意默认的\会被转义，所以改用/
filePath = 'E:/恒大会员导入/处理后_20200721.xlsx'
print(filePath.split('.')[0])

print('开始读取... ')
startReadTime = datetime.datetime.now()

import pandas as pd

data = pd.read_excel(filePath)

endReadTime = datetime.datetime.now()
print('读取完成，耗时 ' + str((endReadTime - startReadTime).seconds) + '秒')

#
rowCount = data.shape[0]
columnCount = data.shape[1]
rowPerFile = 10000

fileCount = rowCount // rowPerFile + 1  # 41

print('共 %s 行数据，将生成 %s 个文件，最后1个文件的行数为 %s' % (rowCount, fileCount, rowCount % rowPerFile))
pieceData0 = data.iloc[0]
pieceData1 = data.iloc[1]

print('处理开始... ')
startProcessTime = datetime.datetime.now()

# 文件名编号从1开始，到42
for i in range(1, fileCount + 1):
    # 填入备注
    data.iloc[(i - 1) * 10000:(i) * 10000, 10] = '20200721-会员导入-' + "{:0>2d}".format(i)  # 每隔1万循环一次
    pieceData = data.iloc[(i - 1) * 10000:(i) * 10000, :]  # 每隔1万循环一次
    # 拼接文件名
    fileName = filePath.split('.')[0] + '-' + str(i) + '.xlsx'
    print(fileName + ' 生成中...')

    # 生成文件
    # to_excel函数的 header 参数默认为0，即取第一行
    # 若不含列名，则设定header = None
    # index 默认为true, 显示index，我们不需要显示，置为False
    pieceData.to_excel(fileName, index=False)
    print(fileName + ' 已生成')

print('文件处理已完成')
endProcessTime = datetime.datetime.now()
print('处理耗时 ' + str((endProcessTime - startProcessTime).seconds) + '秒')
