#!/usr/bin/python3
# Coding: UTF-8
"""
# Created On: 2021/5/15 20:33
# Author: biaobro
# Project: M_003_YJ_Card_Data_Process
# File Name: my_redirector_01.py
# Description:
"""

import sys
import tkinter


class MyStdout:
    def __init__(self, target):
        # save current output obj
        self.target = target
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        # redirect
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info is the output received by sys.stdout and sys.stderr
        # insert the info in last line
        self.target.insert('end', info)

        # show new info
        self.target.update()

        # always locate at the last line
        self.target.see(tkinter.END)

    def restoreStd(self):
        # recover source output
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

    def flush(self):
        pass
