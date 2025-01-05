# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 13_excel split with xlwings.py
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:08
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:08 
@Version            : 1.0
@Description        : None
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:05:44 2020

@author: weibiao.wb
"""

srcFileName = "E:/恒大会员导入/1004/处理后_20201004-1.xlsx"
rowsPerFile = 10000

import xlwings as xw
import datetime

print('开始处理... ')
processStartTime = datetime.datetime.now()

currDate = datetime.datetime.now().strftime("%Y%m%d")

app = xw.App(visible=False, add_book=False)
app.display_alerts = False  # 不显示Excel消息框
app.screen_updating = False  # 关闭屏幕更新,可加快宏的执行速度
srcWookbook = app.books.open(srcFileName)
print(srcWookbook.fullname)  # 输出打开的excle的绝对路径
srcSheet = srcWookbook.sheets[0]

shape = srcSheet.range('A1').current_region.shape
print(shape)

# 确认行数是否为1万的整倍数，如果不是，生成的文件数量需要+1
if ((shape[0] % rowsPerFile) != 0):
    fileCount = shape[0] // rowsPerFile + 1
else:
    fileCount = shape[0] // rowsPerFile
print('There are {:d} rows, {:d} files will be generated.'.format(shape[0], fileCount))

# i默认从0开始
for i in range(fileCount):
    newFileName = srcFileName.split('.')[0] + '-' + str(i + 1) + '_new.xlsx'
    newWookbook = xw.Book()

    # 选择sheet，可以用序号，也可以用名称
    newSheet = newWookbook.sheets[0]

    # 设置第一行，标题
    newSheet.range("A1").value = srcSheet.range("A1:R1").value

    # 复制，粘贴
    srcSheet.range((i * rowsPerFile + 2, 1), ((i + 1) * rowsPerFile + 1, 18)).copy()
    newSheet.range('A2').paste(paste='all_using_source_theme')

    # 备注在第11列
    newSheet.range((2, 11), (rowsPerFile + 1, 11)).value = currDate + "-会员导入-" + "{:0>2d}".format(i + 1)  # 每隔1万循环一次

    newSheet.range('A2').current_region.api.ClearFormats()
    newSheet.range('A1').select()
    newSheet.autofit('c')

    newWookbook.save(newFileName)
    newWookbook.close()
    print(".", end='', flush=True)

srcWookbook.close()
app.screen_updating = True
app.quit()  # 退出excel程序，

processEndTime = datetime.datetime.now()
print('处理完成,耗时 ' + str((processEndTime - processStartTime).seconds) + '秒')
