# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:29:29 2020

@author: weibiao.wb
"""
import datetime

currTime = datetime.datetime.now().strftime("%Y%m%d")

commentsPerFile = currTime + "-会员导入-"

# 每个文件行数，允许最大值10000，默认最大值
rowsPerFile = 10000

# 将要生成的文件数量
fileCount = 5

# 文件名
fileName = 'E:\HengDa\project\处理后_20201004-1_new.xlsx'
