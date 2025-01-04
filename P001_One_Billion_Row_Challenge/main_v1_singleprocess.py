# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : main.py
@Project            : 1 Billion Row Challenge
@CreateTime         : 2024/11/17 00:14
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/11/17 00:14
@Version            : 1.0
@Description        : None
"""
from collections import defaultdict


def create_default_city_data():
    # inf 表示正无穷大， -inf 表示负无穷
    return {'min': float('inf'), 'max': float('-inf'), 'sum': 0.0, 'count': 0}


def process_data(data):
    city_data = defaultdict(create_default_city_data)
    for line in data:
        city, temp = line.strip().split(';')
        temp = float(temp)

        if temp < city_data[city]['min']:
            city_data[city]['min'] = temp
        if temp > city_data[city]['max']:
            city_data[city]['max'] = temp

        city_data[city]['sum'] += temp
        city_data[city]['count'] += 1
    return city_data


if __name__ == '__main__':
    with open('measurements.txt', 'r') as file:
        city_data = process_data(file)

    sorted_city_data = sorted(city_data.items())

    for city, data in sorted_city_data:
        avg = data['sum']/data['count']
        print(f"{city}, {data['min']}/{data['max']}/{avg:1f}")
