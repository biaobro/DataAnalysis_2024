# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : main_v4_polars_singleprocess.py
@Project            : 1 Billion Row Challenge
@CreateTime         : 2024/11/17 20:21
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/11/17 20:21 
@Version            : 1.0
@Description        : None
"""
import time
import polars as pl

t0 = time.time()

df = pl.scan_csv(
    "measurements.txt",
    separator=";",
    has_header=False,
    with_column_names=lambda cols:["city", "value"]
)

grouped = df.group_by("city").agg(
    pl.min("value").alias("min"),
    pl.mean("value").alias("mean"),
    pl.max("value").alias("max")
).sort('city').collect(streaming=True)

for data in grouped.iter_rows():
    print(f"{data[0]}={data[1]:.1f}/{data[2]:.1f}/{data[3]:.1f},", end=" ")

print(f"\n\nElapsed time: {time.time() - t0:.2f} seconds")

