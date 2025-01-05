# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : oristar_utils.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:01
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:01 
@Version            : 1.0
@Description        : None
"""

import base64

# pip install pycryptodome
from Crypto.Cipher import AES
import random


# 如果text不足16位的倍数就用空格补足为16位
# 不同于JS，pycryptodome库中加密方法不做任何padding，因此需要区分明文是否为中文的情况
def add_to_16_cn(text):
    pad = 16 - len(text.encode('utf-8')) % 16
    text = text + pad * chr(pad)
    return text.encode('utf-8')


# 加密函数
def encrypt(text, key, mode=AES.MODE_ECB):
    try:
        text = add_to_16_cn(text)
        key = key.encode('utf-8')
        # print("key is {}".format(key))
        cryptos = AES.new(key, mode)
        cipher_text = cryptos.encrypt(text)
        return base64.b64encode(cipher_text).decode('utf-8')  # base编码
    except Exception:
        print('password bytes length insufficient, please check.')


def genUUID():
    srcList = list("xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")

    for i in range(len(srcList)):
        if srcList[i] == 'x' or srcList[i] == 'y':
            srcList[i] = hex(int(16 * random.random()) | 0).replace('0x', '')

    # print("".join(srcList))
    return "".join(srcList)
