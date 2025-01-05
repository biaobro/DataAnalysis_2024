# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : main.py
@Project            : M_004_YJ_Crawler
@CreateTime         : 2023/3/5 23:04
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 23:04 
@Version            : 1.0
@Description        : None
"""

"""
新版和旧版的思路基本一致，只是在细节处理上有所不同
没有太多考虑容错机制，实际每段代码都需要考虑异常退出
所以，还是有进一步抽象和优化的空间
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.gui import *

if __name__ == '__main__':
    # application 对象
    app = QApplication(sys.argv)

    # QMainWindow对象
    mainwindow = QMainWindow()

    # 这是qt designer实现的Ui_MainWindow类
    ui_components = Ui_mainWindow()

    # 调用setupUi()方法，注册到QMainWindow对象
    ui_components.setupUi(mainwindow)

    # 显示
    mainwindow.show()

    sys.exit(app.exec_())
