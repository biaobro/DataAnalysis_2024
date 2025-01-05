#!/usr/bin/python3
# Coding: UTF-8
"""
# Created On: 2021/5/15 19:05
# Author: biaobro
# Project: M_003_YJ_Card_Data_Process
# File Name: thread_it.py
# Description:
"""
# pack the func into thread
from threading import Thread


def thread_it(func, *args):
    # create thread
    t = Thread(target=func, args=args)
    # enable daemon !!!
    # True 表示主进程（主程序）退出时，不需要等待子进程，避免退不出程序
    t.daemon = True
    # start the thread
    t.start()
    # block
    # t.join()
