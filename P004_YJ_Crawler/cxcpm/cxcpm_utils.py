# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cxcpm_utils.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:01
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:01 
@Version            : 1.0
@Description        : None
"""

import random
import math
import Crypto.Random
import time
import requests
from urllib.parse import urlparse, parse_qs
from cxcpm import cxcpm_basicInfo
from general.general_basic import *


def get_randomByTime():
    # 数组在JS代码里是写死的
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 10在JS代码里也是写死的，
    # Python 中的 range() 是 左闭右开
    for i in range(10, 1, -1):
        idx = math.floor(random.random() * 10)
        tmp = arr[idx]
        arr[idx] = arr[i - 1]
        arr[i - 1] = tmp

    result = 0
    for i in range(5):
        result = result * 10 + arr[i]

    # JS代码：(+new Date()) Date() 结果是字符串，+转成数字
    result = str(result) + str(int((time.time() * 1000)))
    # print("return from getRandomByTime() : " + str(result))
    return result


# 对应JS中的genUUID
def get_UUID(userAgent, pgv_pvi, tencentSig, referrer, href):
    # 参照网站上的格式，有两个值后面是有分号和空格的
    # ISSESSION 写死
    IESESSION = 'alive; '

    pgv_pvi = pgv_pvi + '; '

    # 格式化字符串
    # 对应JS 中的r
    r_in_js = "{}IESESSION={}pgv_pvi={}tencentSig={}{}{}".format(userAgent, IESESSION, pgv_pvi, tencentSig, referrer,
                                                                 href)
    # print(r_in_js)

    # 下面实现对 result 的处理
    # JS 代码 ：W(w() ^ 2147483647 & ge(r)) + "." + this.random()
    e_in_js = base36_encode(w() ^ cxcpm_basicInfo.random_seed & ge(r_in_js)) + "." + thisRandom()

    print("get_UUID() output : {}".format(e_in_js))
    return e_in_js


# 对应JS代码中的ge(函数）
def ge(srcStr):
    e = 1
    if srcStr:
        e = 0

        # JS代码：(r = t.length - 1; r >= 0; r--)
        for index in range(len(srcStr) - 1, -1, -1):

            # JS代码：n = t.charCodeAt(r),
            # 作用是返回指定位置的字符的 Unicode 编码
            # 在python 中的对应函数是 ord
            n = ord(srcStr[index])
            e = (e << 6 & 268435455) + n + (n << 14)
            n = 266338304 & e

            # JS代码：e = 0 != n ? e ^ n >> 21 : e
            # 0 ! = n 得到 True 或者 False
            # JS代码比较难懂：通过在 console 的测试，发现分两步
            # 第1步： 0 != n ? e ^ n >> 21 : e
            # 第2步： 将第1步的值 赋值给 e
            if 0 != n:
                e = e ^ n >> 21
            else:
                e = e
    # 最终得到的值 与 JS代码得到的值一致
    # print("return from ge() : " + str(e))
    return e


# 对应JS代码里的 w() 函数
def w():
    r_byte = Crypto.Random.get_random_bytes(4)
    r_int = int.from_bytes(r_byte, 'big')
    # print(r_int)
    result = cxcpm_basicInfo.random_seed & r_int
    # print("return from w() : " + str(result))
    return result


# 对应JS代码里的 W() 函数
# 将10进制数 转成 36进制
# 36进制 = 26个字母 + 10个数字
def base36_encode(number):
    num_str = '0123456789abcdefghijklmnopqrstuvwxyz'
    if number == 0:
        return '0'

    base36 = []
    while number != 0:
        number, i = divmod(number, 36)  # 返回 number// 36 , number%36
        base36.append(num_str[i])

    result = ''.join(reversed(base36))
    # print("return from base36_encode() : " + result)
    return result


# 对应JS中的自定义函数 random()
# JS 中的自定义函数 random() ，实际又调用了y() + W(+new DatrRe)
# JS 中的 y() 实际只是 return w().toString(36) —— 调用w() 然后做36进制编码
def thisRandom():
    # JS代码：w().toString(36) + "." + W(+new Date)
    result = base36_encode(w()) + "." + base36_encode(int((time.time() * 1000)))
    # print("return from thisRandom() : " + result)
    return result


# 得到 _qddaz
def get_qddaz(userAgent, pgv_pvi, tencentSig, referrer, href):
    prefix = "QD."

    # 对应JS代码中的 t
    t_in_js = prefix + get_UUID(userAgent, pgv_pvi, tencentSig, referrer, href)

    result = t_in_js
    print("get_qddaz() output : {}".format(result))
    return result


# 得到locationHref 后缀是a+一串数字
def get_locationHref():
    # 模拟交互第1步，得到 window.location.href
    # JS代码：window.location.href = '/?a='+ Math.random();
    result = cxcpm_basicInfo.url_host + '/?a=' + str(random.random())
    print("get_locationHref() output : {}".format(result))
    return result


# 得到 tencentSig
def get_tencentSig():
    # JS代码：Math.round((Math.random()||0.5) * 2147483647) * (+new Date())) % 10000000000;
    # 随机数四舍五入 -> 乘法 -> 取整 ->
    # +new Date() -> 时间转换成Unix时间戳
    # % -> 取模运算
    # python 中的 time.time()  得到是10位秒浮点数，转换为毫秒
    result = round(random.random() * cxcpm_basicInfo.random_seed) * int((time.time() * 1000)) % 10000000000
    print("get_tencentSig() output : {}".format(result))
    return result


# 解析 cookies,
# response.cookie 类型是 RequestsCookieJar
# 但是在当前这个场景中 我们希望简化为想要的形式,直接输出为字符串
# 第一个参数为 response.cookies
# 第二个参数为 域名不带协议
def get_cookiesValue(cookie_jar):
    cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)
    found = ['%s=%s' % (name, value) for (name, value) in cookie_dict.items()]
    return ';'.join(found)


# 将url 转换成字典
def url2Dict(url):
    query = urlparse(url).query
    # print(type(query))
    # print(query)
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])
