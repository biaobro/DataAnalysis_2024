# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : general_basic.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 22:55
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 22:55 
@Version            : 1.0
@Description        : None
"""

import logging
import datetime

log_file = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d') + '.log'
data_logger = logging.getLogger(log_file)
print = data_logger.info

notLoginPrompt = 'not logged in, please login first.'
