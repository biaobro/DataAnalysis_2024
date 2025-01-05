#!/usr/bin/python3
# Coding: UTF-8
"""
# Created On: 2021/5/15 12:45
# Author: biaobro
# Project: M_003_YJ_Card_Data_Process
# File Name: 20210515_001.py
# Description:
"""
import logging
# from tkinter import *
from tkinter import Tk
from tkinter import Frame
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from threading import Event
import time
import sys
import my_mergedata
import my_thread
import my_redirector
import my_logger

# event used for communication between Threads
# 用于线程之间通信的 event
event_read = Event()
event_merge = Event()
event_check = Event()

# should be used for all the dict in whole project to keep data structure consistent
dict_keys = ['member', 'member_card', 'pwd', 'chip_card']
log_file = 'all.log'


def file_next_process(file_dict):
    # create instance
    m = my_mergedata.MergeData(file_dict=file_dict)
    try:
        m.get_df()
    except ValueError:
        # error when pandas read file
        event_read.set()
        return

    # check data header
    check = m.check_columns()
    if check is not True:
        # False when some columns missing
        event_check.set()
        return

    measured_card_df = m.measured_card()
    if measured_card_df is not None:
        m.df_to_excel(df=measured_card_df, set_dir='data_after/measured_card.xlsx')

    m_df = m.merge_df()
    m.df_to_excel(m_df)

    # set merge flag to true while all done success
    event_merge.set()


def center_window(target, width, height):
    screenwidth = target.winfo_screenwidth()
    screenheight = target.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    # print(screenwidth, screenheight, size)
    target.geometry(size)


def logger_init():
    # 创建 my_logger 实例
    log = my_logger.MyLogger(filename=log_file, level='info')
    log.logger.info('请选择文件')
    return log.logger


class MyGUI:
    def __init__(self, root):
        self.log = None
        self.button_text_list = ['会员', '会员卡', '卡密', '卡芯片号']
        self.file_dict = {key: None for key in dict_keys}
        self.entry_text_dict = {}
        self.entry_dict = {}
        self.button_dict = {}

        self.initGUI(root)

    # select file dialog
    def select_file(self, i):
        # create file select dialog and set filter
        filename = tkinter.filedialog.askopenfilename(filetypes=[('Excel', '.xls .xlsx')], defaultextension='.xlsx')
        # check file then set entry if file name not null
        if filename != '':
            self.entry_text_dict[i].set(filename)

    # make sure all request file been select
    # and retrieve the file name to file_dict
    # 文件预处理，判断是否全部提供，以及文件名称是否对应，不处理文件内数据
    def file_pre_check(self):
        for i, button_text in enumerate(self.button_text_list):
            # print(i, button_text)
            # 获取文件选择框提供的文件名
            filename = self.entry_dict[i].get()

            # 4个文件必须全部选择，否则只要有1个为空，就返回 False
            if filename == '':
                # entry is empty, no file selected
                self.log.info("文件缺失，退出处理，请确认4个文件全部添加")
                return False
            else:
                # button_text and filename should match strictly?
                if button_text in filename:
                    self.file_dict[list(self.file_dict.keys())[i]] = filename
                    self.log.info(list(self.file_dict.keys())[i] + ' 文件名匹配：成功')
                else:
                    # the selected file does not match with request
                    self.log.info(list(self.file_dict.keys())[i] + ' 文件名匹配：失败，请确认')
                    return False
        return True

    # ui update after process button click
    # make sure not stuck by background data read and process
    # ui 显示，要放到单独1个线程中运行，否则会卡死。在这里持续监测几个事件的标志位，根据结果做进一步处理
    def ui_process(self):
        # disable the Process button while processing
        self.button_process.config(state=tkinter.DISABLED)
        i = 0
        # Update status while begin to process and event_read = False and event_merge = False
        # event_read = True, when read error
        # event_merge = True, when merge done
        while not event_merge.isSet():
            time.sleep(1)
            i += 1
            self.log.info("处理中已耗时" + str(i) + "秒")
            if event_read.isSet():  # pd.read_excel
                self.log.info("文件读取：错误，停止处理。请检查文件内容")
                break
            if event_check.isSet():  # check excel column
                self.log.info("字段检查：错误，停止处理。请检查文件内容")
                break

        # show finished message only if the flags satisfied
        if not event_read.set() and event_merge.isSet():
            self.log.info("文件处理：完成，请到data_after目录查收合并后的文件")

        # clear all event flags when thread exit
        event_read.clear()
        event_merge.clear()
        event_check.clear()

        # recover the Process button whatever
        self.button_process.config(state=tkinter.NORMAL)

    def process(self):
        # check file
        # 对文件是否满足要求（添加文件，以及文件名称合乎要求）做预检
        if not self.file_pre_check():
            return

        # 如果文件预检通过，就启动2个线程，1个负责处理ui 展示，1个负责后台数据处理
        # start file process only if no file is empty
        # thread used to process ui
        my_thread.thread_it(self.ui_process)
        # thread used to process file
        my_thread.thread_it(file_next_process, self.file_dict)

    # 文件：button 和 entry 有规律、成对出现
    # 每个按钮绑定的事件处理函数都单独放进1个线程，避免卡死
    # 注意这里的写法，为了向线程传入参数，使用了 lambda
    def create_widget(self, target):
        for widget_id, button_text in enumerate(self.button_text_list):
            # print(widget_id, button_text)
            # from tkinter.ttk import * the button will be imported as ttk which doesn't support height
            # so use tkinter.button explicitly
            self.button_dict[widget_id] = tkinter.Button(target, width=10, height=2,
                                                         text=self.button_text_list[widget_id],
                                                         font=("Arial", 10, "bold"),
                                                         command=lambda i=widget_id: my_thread.thread_it(
                                                             self.select_file, i))
            self.button_dict[widget_id].place(x=20, y=30 + 70 * widget_id)

            self.entry_text_dict[widget_id] = tkinter.StringVar()

            self.entry_dict[widget_id] = tkinter.Entry(target, textvariable=self.entry_text_dict[widget_id],
                                                       font=("Arial", 10, "bold"),
                                                       state=tkinter.DISABLED)
            self.entry_dict[widget_id].place(x=130, y=30 + 70 * widget_id, width=620, height=43)

    def procedure_quit(self):
        self.root.destroy()

    def initGUI(self, root):
        self.root = root
        self.root.title("tk")
        center_window(self.root, 800, 600)

        # 固定窗口大小
        self.root.resizable = False

        # Notebook belong to ttk
        # tkinter 的组织结构 root -> notebook -> frame -> 各种组件
        self.notebook = ttk.Notebook(self.root)
        self.frame_coupon = Frame()
        self.frame_card = Frame()

        # 创建成对的文件选择按钮 和 文件名称展示框
        self.create_widget(self.frame_card)

        # create process button
        self.button_process = tkinter.Button(self.frame_card, text="处理",
                                             font=("Arial", 12, "bold"),
                                             command=self.process)
        self.button_process.place(x=250, y=300, width=100, height=50)

        # create exit button
        self.button_exit = tkinter.Button(self.frame_card, text="退出",
                                  font=("Arial", 12, "bold"),
                                  command=self.procedure_quit)
        self.button_exit.place(x=450, y=300, width=100, height=50)

        # 创建1个文本框，用于显示 log
        self.text_log = ScrolledText(self.frame_card, width=45, height=13)
        self.text_log.pack(side="bottom", fill=tkinter.BOTH, padx=20, pady=10)

        # 创建 my_redirector 实例
        # 将 Stdout 重定向到 文本款
        my_redirector.MyStdout(self.text_log)
        self.log = logger_init()

        # first tab for card
        self.notebook.add(self.frame_card, text='卡')

        # reserve second tab for coupon
        # notebook.add(frame_coupon, text='券')
        self.notebook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        root.mainloop()


if __name__ == "__main__":
    root = Tk()
    myGUI = MyGUI(root)
