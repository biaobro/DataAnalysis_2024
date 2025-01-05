# -*- coding: utf-8 -*-
import pandas as pd
import os
import shutil
from general.general_basic import *
import xlrd
import warnings
warnings.filterwarnings('ignore')

# 新/旧版 都会用到文件这些功能，所以再抽象出来

def excelFileCombine(filePath, deleteSrcFolder='Y'):
    """
    :param filePath: the folder which only contains the excels
    :param deleteSrcFolder: whether or not delete the folder, default is Yes
    :return:
    """
    # 返回目录下的全部文件名
    dirList = os.listdir(filePath)
    if not dirList:
        # return
        print("folder check failed. please contact technical support. ")
        # exit()
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # 这步 在此处没有什么必要，因为几乎都是同时生成。主要是之前有手动下载文件的场景用过，留着也不影响
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dirList = sorted(dirList, key=lambda x: os.path.getmtime(os.path.join(filePath, x)))
        # print(dir_list)
        # return dir_list

    # 定义一个列表用来放合并的文件名
    fileList = []

    # 遍历文件列表 用pandas 读入
    for info in dirList:
        domain = os.path.abspath(filePath)
        info = os.path.join(domain, info)
        # print('reading : {}'.format(info))

        # 全部字段以文本格式读取,避免科学计数法导致问题
        file = pd.read_excel(info, dtype=str, engine="xlrd")
        fileList.append(file)

    # 合并数据
    # pandas.concat 的强大就在于自动匹配字段名，同时忽略后续文件的表头
    # print('file combining, please wait ...')
    dfCombine = pd.concat(fileList, ignore_index=True)
    # print('file combining done, please check ...')

    # 生成合并后的文件,不需要写入index
    # dfCombine.to_excel(fileName, index=False)

    # 是否删除源文件，默认为N
    # os.rmdir 只能删除空文件夹
    # shutil 删除目录以及文件
    if deleteSrcFolder == 'Y':
        shutil.rmtree(filePath)
        # print('clean temp files done.')

    # 返回 dataFrame
    return dfCombine


'''
说明：
1,输入dataFrame,输出xlsx
2,增加了格式设置，将单元格格式从 【常规】设置为【文本】
3,自动列宽没有实现，xlsxwriter 官方不支持 autofit column. 
4,有个第三方包Aspose.Cells，没来得及研究怎么使用
'''
def excelFileGenerate(df, fileName):
    """
    :param df: pandas.DataFrame
    :param fileName:
    :return: True(success) or False(fail)
    """
    try:
        print('write {} start.'.format(fileName))
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        cell_format = workbook.add_format({'num_format': '@'})

        # xlsxwriter does not support autofit column set
        worksheet.set_column(first_col=0, last_col=df.shape[1], cell_format=cell_format)
        writer.save()
        print('write {} done.'.format(fileName))
    except Exception as e:
        print(e)
        return False
    else:
        return True
