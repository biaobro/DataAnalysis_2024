# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:11:52 2020

@author: weibiao.wb
"""
import globalVariable
import time
import xlwings as xw
import datetime
import pythoncom


def producer_drop(out_q, tkWindow):
    out_q.put((globalVariable.fileCount, tkWindow))
    for i in range(1, globalVariable.fileCount + 1):
        print("%s: %d, %s \n" % ("producer", i, time.ctime(time.time())))
        time.sleep(2)
        out_q.put((i, tkWindow))


def producer(out_q, tkWindow):
    pythoncom.CoInitialize()
    print('开始处理... ')
    # processStartTime = datetime.datetime.now()

    currTime = datetime.datetime.now().strftime("%Y%m%d")

    excelApp = xw.App(visible=False, add_book=False)
    excelApp.display_alerts = False  # 不显示Excel消息框
    excelApp.screen_updating = False  # 关闭屏幕更新,可加快宏的执行速度

    # fileNameAfterProcess = globalVariable.fileName.replace('\\',"/")
    wb = excelApp.books.open(globalVariable.fileName)
    print(wb.fullname)  # 输出打开的excel的绝对路径
    sht = wb.sheets[0]

    shape = sht.range('A1').current_region.shape
    print(shape)
    print('There are {:d} rows, {:d} files will be generated.'.
          format(shape[0], shape[0] // globalVariable.rowsPerFile + 1))

    tkWindow.textLogOutput.insert('end', 'There are {:d} rows, {:d} files will be generated.'.
                                  format(shape[0], shape[0] // globalVariable.rowsPerFile + 1));

    # print(sht.range('A1').current_region.rows.count)
    globalVariable.fileCount = shape[0] // globalVariable.rowsPerFile + 1
    out_q.put((globalVariable.fileCount, tkWindow))

    for i in range(1, shape[0] // globalVariable.rowsPerFile + 2):
        print("%s: %d, %s \n" % ("producer : ", i, time.ctime(time.time())))
        newFileName = globalVariable.fileName.split('.')[0] + '-' + str((i)) + '_new.xlsx'
        newWb = xw.Book()
        newSheet = newWb.sheets['sheet1']

        newSheet.range("A1").value = sht.range("A1:R1").value

        sht.range(((i - 1) * globalVariable.rowsPerFile + 2, 1),
                  (i * globalVariable.rowsPerFile + 1, 18)).copy()
        newSheet.range('A2').paste(paste='all_using_source_theme')

        # range((2,18),(globalVariable.rowsPerFile+1,18))
        # range('K2:K10001')
        newSheet.range((2, 11), (globalVariable.rowsPerFile + 1, 11)).value = currTime + "-会员导入-" + "{:0>2d}".format(
            i)  # 每隔1万循环一次
        newSheet.range('A2').current_region.api.ClearFormats()
        newSheet.range('A1').select()
        newSheet.autofit('c')
        newWb.save(newFileName)

        newWb.close()
        out_q.put((i, tkWindow))
        # print(".",end = '',flush = True)

    wb.save()
    wb.close()
    excelApp.screen_updating = True
    excelApp.quit()  # 退出excel程序，
    # app.kill()
    # processEndTime = datetime.datetime.now()
    # print('处理完成,耗时 ' + str((processEndTime - processStartTime).seconds) + '秒')
    pythoncom.CoUninitialize()


def consumer(in_q):
    i = 0
    while True:
        data, tkWindow = in_q.get()
        print("consumer", data)
        # 第1个值是用来设置进度条最大值
        if i == 0:
            tkWindow.progressBar['maxim'] = data
            print("set maxim value")
        # 后续值才是进度条的实时值
        else:
            print("set progressbar")
            tkWindow.progressBar['value'] = data
            tkWindow.root.update()
            time.sleep(0.1)
            if data == globalVariable.fileCount:
                print("exit")
                i = 0
                tkWindow.buttonSelectFile["state"] = 'normal'
                tkWindow.checkButtonRowsModify['state'] = 'normal'
                break
        i += 1
