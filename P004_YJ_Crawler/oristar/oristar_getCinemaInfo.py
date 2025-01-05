# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_getCinemaInfo.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2022/6/21 15:42
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2022/6/21 15:42
@Version            : 1.0
@Description        : None
"""

import requests
import json

from oristar import oristar_basicInfo
from general.general_basic import *


def getCinemaInfo():
    # 新版在这里使用的是 get 方法
    try:
        response = requests.get(url=oristar_basicInfo.url_cinemaInfo,
                                headers=oristar_basicInfo.headers)
    except Exception as e:
        print(e)
        return False

    if response.status_code == 200:
        print("get cinemaInfo success")

        # 返回信息中包含 影城名称 ID  影城8位专资编码
        # print(response.text)

        # 将字符串response.text转换成字典
        # json_data = json.loads(response.text)

        # response.text 是字符串格式
        # json_data = json.loads(response.text) 得到是字典格式
        # json_data['data'] 得到是 list 格式，形式是方括号括起来的花括号[{}]，list 只能通过数字下表获取
        # json_data['data'][0] 得到的就是{}，这个是字典格式
        target_data = json.loads(response.text)['data'][0]
        # print(target_data)
        # print(type(target_data))

        # 得到8位编码
        oristar_basicInfo.cinemaCode = target_data['code']
        print("cinema code : {}".format(oristar_basicInfo.cinemaCode))

        # 得到影城名称
        oristar_basicInfo.cinemaName = target_data['name']
        print("cinema name : {}".format(oristar_basicInfo.cinemaName))

        # 得到系统开通时间
        # 新版直接返回字符串格式的开通时间
        oristar_basicInfo.cinemaSystemInitTime = target_data['createTime']
        print("cinema system init time : {}".format(oristar_basicInfo.cinemaSystemInitTime))
    else:
        print('get cinemaInfo failed, please contact technical support.')
        # exit()



# oristar_login.login()
# getCinema()

