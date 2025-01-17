# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : gui.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:04
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:04 
@Version            : 1.0
@Description        : None
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_v0.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import math

from PyQt5 import QtCore, QtGui, QtWidgets

from cxcpm import cxcpm_basicInfo, cxcpm_getCoupon, cxcpm_login, cxcpm_getCinemaInfo
from general import general_redirector, general_logger, general_thread
from general.general_basic import *
from oristar import oristar_login, oristar_basicInfo, oristar_getCinemaInfo, oristar_getCoupon

'''
@20220119 
1,循环实现 label 和 输入框组件创建和配置，精简代码
2,整合2个退出按钮的代码 procedure_quit 

@20220120
1,循环实现 按钮创建
2,注意事件函数的不同处理方法
3,循环实现 tabWidget 创建
4,在前面基础上，实现全部组件的循环创建，减少代码100+行

@20220121
1,更新了按钮clicked事件的处理逻辑，定义函数字典，增加灵活性
2,解决了线程使用问题，处理cxcpm 登录时，不再因为耗时显示"未响应"，不再"假死"
3,解决了打印不能及时显示的问题，在general_redirector 中将打印操作也放到线程中处理。
'''


# log_file = 'all.log'
def logger_init():
    log = general_logger.Logger(filename=log_file, level='info')
    print('logger init done. ')
    print('Welcome to crawler world.')
    return log.logger


class Ui_mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.log = None

        # tab
        self.tabWidgetNames = ['oristar', 'cxcpm']
        self.qTabWidgetDict = {}

        # widgetNames used for label and line edit
        self.labelNames = self.lineEditNames = ['customerCode', 'loginName', 'password']

        self.qLabelDictList = [dict() for x in range(len(self.tabWidgetNames))]
        self.qLineEditDictList = [dict() for x in range(len(self.tabWidgetNames))]

        # btnNames
        self.btnNames = ['Login', 'Exit', 'GetCinemaInfo', 'GetCoupon']
        self.qButtonDictList = [dict() for x in range(len(self.tabWidgetNames))]

        # function dict used to keep button-handler relations
        self.funcDict = {
            '00': self.oristar_btnLoginClicked,
            '01': self.btnExitClicked,
            '02': self.oristar_btnGetCinemaInfoClicked,
            '03': self.oristar_btnGetCouponClicked,
            '10': self.cxcpm_btnLoginClicked,
            '11': self.btnExitClicked,
            '12': self.cxcpm_btnGetCinemaInfoClicked,
            '13': self.cxcpm_btnGetCouponClicked,
        }

    def btnClicked(self):
        """test"""
        print('Begin')
        # print(1/0)   #人为地引发一个异常，程序直接退出了，控制台出现了`Unhandled Python exception`错误

    # 点击登录按钮后先判断是否填写全部信息
    def oristar_btnLoginClicked(self):
        # 同时检查3个输入框是否非空
        if all([oristar_basicInfo.loginPayLoad['customerCode'],
                oristar_basicInfo.loginPayLoad['loginName'],
                oristar_basicInfo.loginPayLoad['password'],
                ]):
            print(oristar_basicInfo.loginPayLoad)
            print("all user info have been get. start processing.")

            # 开始处理登录请求
            oristar_login.login()

            # 如果登录成功，将登录按钮置灰
            if oristar_basicInfo.loginStatus:
                print('now disable login button.')
                self.qButtonDictList[0][0].setEnabled(False)
        else:
            print("please input all request info.")

    def oristar_btnGetCinemaInfoClicked(self):
        if oristar_basicInfo.loginStatus:
            oristar_getCinemaInfo.getCinemaInfo()
        else:
            print(notLoginPrompt)

    def oristar_btnGetCouponClicked(self):
        if oristar_basicInfo.loginStatus:
            oristar_getCoupon.getCoupon()
        else:
            print(notLoginPrompt)

    # 退出
    def btnExitClicked(self):
        QtCore.QCoreApplication.instance().quit()

    # 点击登录按钮后先判断是否填写全部信息
    def cxcpm_btnLoginClicked(self):

        # 同时检查3个输入框是否非空
        if all([cxcpm_basicInfo.loginPayLoad['customerCode'],
                cxcpm_basicInfo.loginPayLoad['loginName'],
                cxcpm_basicInfo.loginPayLoad['password'],
                ]):
            print(cxcpm_basicInfo.loginPayLoad)
            print("all user info have been get. start processing.")

            # 开始处理登录请求
            # 注意
            cxcpm_login.login()

            # 如果登录成功，将登录按钮置灰
            if cxcpm_basicInfo.loginStatus:
                print('now disable login button.')
                self.qButtonDictList[1][0].setEnabled(False)
        else:
            print("please input all request info.")

    def cxcpm_btnGetCinemaInfoClicked(self):
        if cxcpm_basicInfo.loginStatus:
            cxcpm_getCinemaInfo.getCinemaInfo()
        else:
            print(notLoginPrompt)

    def cxcpm_btnGetCouponClicked(self):
        if cxcpm_basicInfo.loginStatus:
            cxcpm_getCoupon.getCoupon()
        else:
            print(notLoginPrompt)

    # 把输入框的 editFinish 事件处理函数抽象成1个
    def basicInfoAssign(self, tabID, widgetId):
        print(
            (self.tabWidgetNames[tabID], self.lineEditNames[widgetId], self.qLineEditDictList[tabID][widgetId].text()))
        if self.tabWidgetNames[tabID] == 'cxcpm':
            cxcpm_basicInfo.loginPayLoad[self.labelNames[widgetId]] = self.qLineEditDictList[tabID][widgetId].text()
        else:
            oristar_basicInfo.loginPayLoad[self.labelNames[widgetId]] = self.qLineEditDictList[tabID][
                widgetId].text()

    # 按钮点击事件 处理方式 A
    def btnClickedProcessA(self):
        sending_button = self.sender()

        print('%s Clicked!' % str(sending_button.objectName()))
        if str(sending_button.objectName()) == "oristar_btnLogin":
            self.oristar_btnLoginClicked()
        elif str(sending_button.objectName()) == "oristar_btnExit":
            self.btnExitClicked()
        elif str(sending_button.objectName()) == "oristar_btnGetCinemaInfo":
            self.oristar_btnGetCinemaInfoClicked()
        elif str(sending_button.objectName()) == "oristar_btnGetCoupon":
            self.oristar_btnGetCouponClicked()
        elif str(sending_button.objectName()) == "cxcpm_btnLogin":
            self.cxcpm_btnLoginClicked()
        elif str(sending_button.objectName()) == "cxcpm_btnExit":
            self.btnExitClicked()
        elif str(sending_button.objectName()) == "cxcpm_btnGetCinemaInfo":
            self.cxcpm_btnGetCinemaInfoClicked()
        elif str(sending_button.objectName()) == "cxcpm_btnGetCoupon":
            self.cxcpm_btnGetCouponClicked()
        else:
            print('The button has no related event handler. ')

    # 按钮点击事件 处理方式 B
    # A 方式需要20行代码，而且僵硬
    # B 方式加上字典定义只需要15行代码，非常灵活
    def btnClickedProcessB(self, tabId, widgetID):
        # 要在外面套1层括号，否则报错："not all arguments converted during string formatting"
        print((self.tabWidgetNames[tabId], self.btnNames[widgetID]))
        funcCode = "{}{}".format(tabId, widgetID)

        # call the function
        self.funcDict[funcCode]()

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 450, 560))

        # font 默认字号9
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)

        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidgetName")

        mainWindow.setWindowTitle("crawler")

        # 外层循环 创建 2个tabWidget
        # 内层循环 创建 3个label, 3个lineEdit, 4个button
        for tabId in range(len(self.tabWidgetNames)):
            self.qTabWidgetDict[tabId] = QtWidgets.QWidget()
            self.qTabWidgetDict[tabId].setObjectName("tab_" + self.tabWidgetNames[tabId])
            # 直接在addTab 里命名，不再调用setTabText
            self.tabWidget.addTab(self.qTabWidgetDict[tabId], self.tabWidgetNames[tabId])

            # 创建 tab_oristar 上的 label 和 单行输入框 组件
            for widgetId, widgetText in enumerate(self.labelNames):
                self.qLabelDictList[tabId][widgetId] = QtWidgets.QLabel(
                    self.tabWidgetNames[tabId] + "_label" + widgetText,
                    self.qTabWidgetDict[tabId])
                self.qLabelDictList[tabId][widgetId].setGeometry(QtCore.QRect(20, 40 + 70 * widgetId, 150, 30))
                self.qLabelDictList[tabId][widgetId].setFont(font)
                self.qLabelDictList[tabId][widgetId].setText(widgetText)

                self.qLineEditDictList[tabId][widgetId] = QtWidgets.QLineEdit(self.qTabWidgetDict[tabId])
                self.qLineEditDictList[tabId][widgetId].setGeometry(QtCore.QRect(160, 40 + 70 * widgetId, 240, 30))
                self.qLineEditDictList[tabId][widgetId].setFont(font)
                self.qLineEditDictList[tabId][widgetId].setClearButtonEnabled(True)
                self.qLineEditDictList[tabId][widgetId].setObjectName(self.tabWidgetNames[tabId] + "_txt" + widgetText)
                self.qLineEditDictList[tabId][widgetId].setPlaceholderText("请输入" + widgetText)

                # 还需要加上事件，lambda 函数中不能直接使用widget_id 需要转
                self.qLineEditDictList[tabId][widgetId].editingFinished.connect(
                    lambda x=tabId, y=widgetId: self.basicInfoAssign(x, y))

            for btnId, btnText in enumerate(self.btnNames):
                self.qButtonDictList[tabId][btnId] = QtWidgets.QPushButton(btnText, self.qTabWidgetDict[tabId])
                self.qButtonDictList[tabId][btnId].setEnabled(True)
                # x,y 坐标变，width 和 height 不变
                # x 和 y 的变化规律不同
                if btnId % 2 == 0:
                    self.qButtonDictList[tabId][btnId].setGeometry(
                        QtCore.QRect(20, 250 + math.ceil(btnId / 2) * 70, 180, 50))
                else:
                    self.qButtonDictList[tabId][btnId].setGeometry(
                        QtCore.QRect(20 + math.ceil(btnId % 2) * 200, 250 + math.floor(btnId / 2) * 70, 180, 50))

                self.qButtonDictList[tabId][btnId].setFont(font)
                self.qButtonDictList[tabId][btnId].setObjectName(self.tabWidgetNames[tabId] + "_btn" + btnText)

                # 这里尝试了3种方式，给点击事件绑定处理函数
                # 1，直接绑定函数
                # 2，每个点击事件创建1个线程，在线程中执行函数处理，判断发送者
                # 3，每个点击事件创建1个线程，在线程中执行函数处理，同时携带发送者信息
                # 在线程中处理目前存在1个问题，打印存在延迟，需要窗口刷新后才能完整显示 —— 未解决
                # self.qButtonDictList[tabId][btnId].clicked.connect(self.btnClickedProcessA)
                # self.qButtonDictList[tabId][btnId].clicked.connect(
                #     lambda btnClickedHandler: general_thread.thread_it(self.btnClickedProcessA))
                # 注意general_thread.thread_it 的使用方法，函数不需要带括号
                self.qButtonDictList[tabId][btnId].clicked.connect(
                    lambda state, x=tabId, y=btnId: general_thread.thread_it(self.btnClickedProcessB, x, y))
                # self.qButtonDictList[tabId][btnId].clicked.connect(
                #     lambda state, x=tabId, y=btnId: self.btnClickedProcessB(x, y))

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(475, 40, 700, 530))
        self.textBrowser.setObjectName("logOutput")

        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())
        # self.textBrowser.

        mainWindow.setCentralWidget(self.centralwidget)

        general_redirector.Redirector(self.textBrowser)
        # thread = general_redirector.Redirector(self.textBrowser)  # create a thread
        # thread.trigger.connect(self.update_text)  # connect to it's signal
        # thread.start()  # start the thread
        self.log = logger_init()

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
