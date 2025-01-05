# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_login.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:00
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:00 
@Version            : 1.0
@Description        : None
"""

import requests
import json

from oristar import oristar_basicInfo, oristar_utils

from general.general_basic import *


# 本函数的实现逻辑，参照网页js代码
# 如js代码由变化，需要调整本代码
# 实现登录，并且从返回信息中得到  'Cpm-User-Token'
# 这里uuid 的生成和截取位数，也是强依赖网站逻辑，请保持高度关注
def login():
    print("login processing, please wait...")
    # 先生成UUID
    uuid = oristar_utils.genUUID()

    # 从uuid中取前16位，得到'Cpm-User-Key'
    oristar_basicInfo.headers['Cpm-User-Key'] = uuid[0:16]
    # print(headers['Cpm-User-Key'])
    # print(oristar_basicInfo.headers)

    # 调用加密函数，得到加密后的密码密文
    # 第1个参数是要被加密的密码明文
    # 第2个参数是要用到的key，由用户名+UUID的前13位拼接组成
    oristar_basicInfo.loginPayLoad['password'] = oristar_utils.encrypt(
        oristar_basicInfo.loginPayLoad['password'],
        (oristar_basicInfo.loginPayLoad['loginName'] + uuid[0:13])
    )

    # print(payLoad['password'])
    # 打印待提交用户信息
    print('payload data after encrypt : ')
    print(oristar_basicInfo.loginPayLoad)

    # 提交请求
    # loginPayLoad 是python 字典格式，需要转成 json 格式
    try:
        response = requests.post(url=oristar_basicInfo.url_login,
                                 headers=oristar_basicInfo.headers,
                                 data=json.dumps(oristar_basicInfo.loginPayLoad))
    except Exception as e:
        print(e)
        return False

    if response.status_code == 200:
        print("login request submit success.")

        json_data = json.loads(response.text)

        # 需要在网页状态码的基础上，进一步判断接口返回中的code
        if json_data['code'] == 200:
            print("login success.")
            oristar_basicInfo.loginStatus = True
            # 从请求返回中得到  Cpm-User-Token
            # response.text 是文本格式
            # response.content 是二进制格式
            # json.loads 把 str 转成 Python 字段
            cpmUserToken = json_data['data']['token']
            # print(cpmUserToken)

            # 直接更新header中的信息？
            oristar_basicInfo.headers['Cpm-User-Token'] = cpmUserToken
            # print(oristarcloud_basicInfo.headers)
            # 也可以考虑返回信息
            return cpmUserToken
        else:
            # 输出登录失败信息，如密码错误，序列号不存在等
            print(json_data['msg'])
            print("login failed. please check the inputs.")
    else:
        # 输出页面请求失败信息
        print(response)
        print("login request failed. please contact technical support.")

        # 在正式代码里，exit() 就直接退出了，所以需要去掉 换成return?
        # exit()
        return False

# login()
