# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 11:18:25 2020

@author: weibiao.wb
"""
import xlwings as xw
import time
import datetime
import pythoncom  # .\pip.exe install pywin32
import globalVariable
import threading

globalLock = threading.Lock()


def unitProcess(srcSheet, i, newFileName, newCommentValue):
    globalLock.acquire()
    pythoncom.CoInitialize()
    print("%s: %d, %s \n" % ("unitProcess : ", i, time.ctime(time.time())))
    # newFileName= savePath + '-' + str(i) + '_new.xlsx'
    newWorkbook = xw.Book()
    destSheet = newWorkbook.sheets[0]

    destSheet.range("A1").value = srcSheet.range("A1:R1").value

    srcSheet.range(((i - 1) * globalVariable.rowsPerFile + 2, 1),
                   (i * globalVariable.rowsPerFile + 1, 18)).copy()
    destSheet.range('A2').paste(paste='all_using_source_theme')

    # range((2,18),(globalVariable.rowsPerFile+1,18))
    # range('K2:K10001')
    # destSheet.range((2,11),(globalVariable.rowsPerFile+1,11)).value = currTime + "-会员导入-" + "{:0>2d}".format(i)#每隔1万循环一次
    destSheet.range((2, 11), (globalVariable.rowsPerFile + 1, 11)).value = newCommentValue
    destSheet.range('A2').current_region.api.ClearFormats()
    destSheet.range('A1').select()
    destSheet.autofit('c')
    newWorkbook.save(newFileName)
    newWorkbook.close()
    pythoncom.CoUninitialize()
    globalLock.release()


if __name__ == "__main__":
    excelApp = xw.App(visible=False, add_book=False)
    excelApp.display_alerts = False  # 不显示Excel消息框
    excelApp.screen_updating = False  # 关闭屏幕更新,可加快宏的执行速度

    # fileNameAfterProcess = globalVariable.fileName.replace('\\',"/")
    srcWorkbook = excelApp.books.open(globalVariable.fileName)
    print(srcWorkbook.fullname)  # 输出打开的excle的绝对路径
    srcSheet = srcWorkbook.sheets[0]

    shape = srcSheet.range('A1').current_region.shape
    if ((shape[0] - 1) % globalVariable.rowsPerFile != 0):
        fileCount = (shape[0] - 1) // globalVariable.rowsPerFile + 1
    else:
        fileCount = (shape[0] - 1) // globalVariable.rowsPerFile

    print('There are {:d} rows, {:d} files will be generated.'.
          format(shape[0] - 1, fileCount))

    savePath = globalVariable.fileName.split('.')[0]
    currDate = datetime.datetime.now().strftime("%Y%m%d")

    threads = []
    for i in range(1, fileCount + 1):
        newFileName = savePath + '-' + str(i) + '_new.xlsx'
        newCommentValue = currDate + "-会员导入-" + "{:0>2d}".format(i)
        t = threading.Thread(target=unitProcess, args=(srcSheet, i, newFileName, newCommentValue))
        threads.append(t)

    startTime = time.time()
    for thr in threads:
        thr.start()

    for thr in threads:
        thr.join()

    print("last time: {} s".format(time.time() - startTime))
    srcWorkbook.close()
    excelApp.screen_updating = True
    excelApp.quit()
