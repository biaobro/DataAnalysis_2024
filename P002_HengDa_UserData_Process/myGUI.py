# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:08:46 2020

@author: weibiao.wb
"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.filedialog
import time
import threading
from queue import Queue
import globalVariable
import myThread
import xlwings as xw

LOG_LINE_NUM = 0


class myApp:
    def __init__(self):  # , root):
        self.root = tk.Tk()
        # setting title
        self.root.title("会员数据处理工具")
        # setting window size
        width = 600
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        ft = tkFont.Font(family='隶书', size=20)

        self.buttonSelectFile = tk.Button(self.root)
        self.buttonSelectFile["bg"] = "#efefef"
        # ft = tkFont.Font(family='Times',size=10)
        self.buttonSelectFile["font"] = ft
        self.buttonSelectFile["fg"] = "#000000"
        self.buttonSelectFile["justify"] = "center"
        self.buttonSelectFile["text"] = "选择文件"
        self.buttonSelectFile.place(x=100, y=20, width=150, height=70)
        self.buttonSelectFile["command"] = self.buttonSelectFile_command

        self.buttonStartProcess = tk.Button(self.root)
        self.buttonStartProcess["bg"] = "#efefef"
        # ft = tkFont.Font(family='Times',size=10)
        self.buttonStartProcess["font"] = ft
        self.buttonStartProcess["fg"] = "#000000"
        self.buttonStartProcess["justify"] = "center"
        self.buttonStartProcess["text"] = "开始处理"
        self.buttonStartProcess["state"] = tk.DISABLED
        self.buttonStartProcess.place(x=340, y=20, width=150, height=70)
        self.buttonStartProcess["command"] = self.buttonStartProcess_command

        labelRows = tk.Label(self.root)
        ft = tkFont.Font(family='仿宋', size=10)
        labelRows["font"] = ft
        labelRows["fg"] = "#333333"
        labelRows["justify"] = "center"
        labelRows["text"] = "行数"
        labelRows.place(x=20, y=100, width=70, height=25)

        self.editRows = tk.Entry(self.root)
        self.editRows["borderwidth"] = "1px"
        # ft = tkFont.Font(family='Times',size=10)
        self.editRows["font"] = ft
        self.editRows["fg"] = "#333333"
        self.editRows["justify"] = "center"
        # self.editRows["text"] = "10000"
        varRows = tk.StringVar()
        varRows.set(1000)
        self.editRows['textvariable'] = varRows
        self.editRows['state'] = tk.DISABLED
        self.editRows.place(x=100, y=100, width=70, height=25)

        self.checkButtonRowsModify = tk.Checkbutton(self.root)
        # ft = tkFont.Font(family='Times',size=10)
        self.checkButtonRowsModify["font"] = ft
        self.checkButtonRowsModify["fg"] = "#333333"
        self.checkButtonRowsModify["justify"] = "center"
        self.checkButtonRowsModify["text"] = "修改"
        self.checkButtonRowsModify["offvalue"] = "0"
        self.checkButtonRowsModify["onvalue"] = "1"
        self.varCheckButtonRowsStatus = tk.IntVar()
        self.varCheckButtonRowsStatus.set(0)
        self.checkButtonRowsModify['variable'] = self.varCheckButtonRowsStatus
        self.checkButtonRowsModify["command"] = self.checkButtonRowsModify_command
        self.checkButtonRowsModify.place(x=190, y=100, width=70, height=25)

        labelComments = tk.Label(self.root)
        # ft = tkFont.Font(family='Times',size=10)
        labelComments["font"] = ft
        labelComments["fg"] = "#333333"
        labelComments["justify"] = "center"
        labelComments["text"] = "备注"
        labelComments.place(x=280, y=100, width=70, height=25)

        self.editComments = tk.Entry(self.root)
        self.editComments["borderwidth"] = "1px"
        # ft = tkFont.Font(family='Times',size=10)
        self.editComments["font"] = ft
        self.editComments["fg"] = "#333333"
        self.editComments["justify"] = "center"
        # self.editComments["text"] = "年月日-会员导入-批次号"
        varComments = tk.StringVar()
        varComments.set('年月日-会员导入-批次号')
        self.editComments['textvariable'] = varComments
        self.editComments['state'] = tk.DISABLED
        self.editComments.place(x=350, y=100, width=200, height=25)

        labelLog = tk.Label(self.root)
        # ft = tkFont.Font(family='Times',size=10)
        labelLog["font"] = ft
        labelLog["fg"] = "#333333"
        labelLog["justify"] = "center"
        labelLog["text"] = "日志"
        labelLog.place(x=20, y=150, width=70, height=25)

        self.textLogOutput = tk.Text(self.root)
        self.textLogOutput["font"] = ft
        self.textLogOutput.place(x=100, y=150, width=450, height=250)

        labelProgress = tk.Label(self.root)
        # ft = tkFont.Font(family='Times',size=10)
        labelProgress["font"] = ft
        labelProgress["fg"] = "#333333"
        labelProgress["justify"] = "center"
        labelProgress["text"] = "进度"
        labelProgress.place(x=20, y=425, width=70, height=25)

        self.progressBar = ttk.Progressbar(self.root)
        self.progressBar['orient'] = tk.HORIZONTAL
        self.progressBar['length'] = 450
        self.progressBar['mode'] = 'determinate'
        self.progressBar['value'] = 0
        self.progressBar['maxim'] = 100
        # self.varProgressValue = tk.IntVar()
        # self.varProgressValue.set(10)
        # self.progressBar['variable'] = self.varProgressValue
        self.progressBar.place(x=100, y=425, width=450, height=25)

    def buttonSelectFile_command(self):
        print("buttonSelectFile_command")
        filename = tk.filedialog.askopenfilename(
            filetypes=[("Microsoft Excel文件", "*.xlsx")],
            defaultextension=".xlsx")
        if filename != '':
            self.textLogOutput.insert(tk.END, "您选择了文件：" + filename + "\n");
            self.progressBar['value'] = 0
            self.buttonStartProcess["state"] = tk.NORMAL
            globalVariable.fileName = filename
            print(globalVariable.fileName)
        else:
            self.textLogOutput.insert(tk.END, "您没有选择任何文件\n");

    def buttonStartProcess_command(self):
        print("buttonStartProcess_command")
        # 需要做的事情
        # 1，获取行数
        globalVariable.rowsPerFile = int(self.editRows.get())
        # 2，获取备注
        # globalVariable.commentsPerFile = self.editComments.get()
        # 3，禁用选择文件按钮
        self.buttonSelectFile["state"] = tk.DISABLED
        # 4，禁用开始处理按钮
        self.buttonStartProcess["state"] = tk.DISABLED
        # 5，禁止编辑行数，备注格式
        self.varCheckButtonRowsStatus.set('0')
        self.editRows['state'] = tk.DISABLED
        self.checkButtonRowsModify['state'] = tk.DISABLED
        # 5，启动进度条
        # 6，启动线程，处理文件

        # 问题：文件处理进程开启后，并不能很快得到行数，而第二个进程依赖行数
        # th0 = threading.Thread()
        # th0.setDaemon(True)
        # th0.start()

        q = Queue()
        th1 = threading.Thread(target=myThread.producer, args=(q, self,))
        th1.setDaemon(True)
        th1.start()

        th2 = threading.Thread(target=myThread.consumer, args=(q,))
        th2.setDaemon(True)
        th2.start()

    def checkButtonRowsModify_command(self):
        print("checkButtonRowsModify_command")
        print(self.varCheckButtonRowsStatus.get())
        if self.varCheckButtonRowsStatus.get() == 1:
            self.editRows['state'] = tk.NORMAL
        else:
            self.editRows['state'] = tk.DISABLED
