# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : main_v2_multiprocess.py
@Project            : 1 Billion Row Challenge
@CreateTime         : 2024/11/17 00:14
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/11/17 00:14 
@Version            : 1.0
@Description        : None
"""
import os.path
import multiprocessing as mp
from collections import defaultdict


def create_default_city_data():
    # inf 表示正无穷大， -inf 表示负无穷
    return {'min': float('inf'), 'max': float('-inf'), 'sum': 0.0, 'count': 0}


def process_data(start_offset, end_offset):
    city_data = defaultdict(create_default_city_data)
    with open('measurements.txt', 'r') as file:
        file.seek(start_offset)
        for line in file:
            start_offset += len(line)
            if start_offset >= end_offset:
                break

            city, temp = line.strip().split(';')
            temp = float(temp)

            if temp < city_data[city]['min']:
                city_data[city]['min'] = temp
            if temp > city_data[city]['max']:
                city_data[city]['max'] = temp

            city_data[city]['sum'] += temp
            city_data[city]['count'] += 1
    return city_data


def get_chunks_position():
    file_size = os.path.getsize('measurements.txt')
    chunk_size = file_size // mp.cpu_count()
    chunk_positions = []
    with open('measurements.txt', 'r') as file:
        for _ in range(mp.cpu_count()):
            start_offset = file.tell()
            file.seek(start_offset + chunk_size)
            file.readline()
            end_offset = file.tell()
            chunk_positions.append((start_offset, end_offset))
    return chunk_positions


def merge_results(results):
    final_data = defaultdict(create_default_city_data)
    for city_data in results:
        for city, data in city_data.items():
            if data['min'] < final_data[city]['min']:
                final_data[city]['min'] = data['min']
            if data['max'] > final_data[city]['max']:
                final_data[city]['max'] = data['max']
            final_data[city]['sum'] += data['sum']
            final_data[city]['count'] += data['count']
    return final_data


if __name__ == '__main__':
    chunk_positions = get_chunks_position()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(process_data, chunk_positions)

    final_data = merge_results(results)

    sorted_city_data = sorted(final_data.items())

    for city, data in sorted_city_data:
        avg = data['sum'] / data['count']
        print(f"{city}, {data['min']}/{data['max']}/{avg:1f}")
