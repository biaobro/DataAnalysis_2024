
Attribute VB_Name = "MaizuoOrderDetails"
'====================================================================================================
'创建日期:  @20180813
'文件描述:  根据原始表生成分类后的支付方式，以便于统计
'           生成支付方式透视表
'修改记录:
'           @20181107   增加支付方式"扫码以及云支付"
'           @20181110   修改支付方式填充公式的写法，改为分行
'                       精简了透视表字段的设置步骤，原先先默认后修改，现在直接使用期望的方式
'           @20181120   简化支付方式的计算公式
'           @20181121   删除前3行，加第5行。增加1列，作为序号（确保每行存在主键）
'           @20181126   修复Bug，之前的程序未考虑"现金"支付方式不存在的情况
'           @20181203   在For Each ... Next循环中增加了 Exit For 语句，执行完相应的操作后就退出。以提高效率
'           @20181206   去除多余的激活和选择操作，少了1步对sheet6的选择以提高效率（Selection.Copy Sheets("Sheet6").Range("A3")）
'           @20181209   增加对ScreenUpdating属性的设置，以节约程序运行时间（约300ms）
'           @20181210   将透视表添加值，和设置格式的操作统一放进With语句中
'                       筛选器区域中增加"项目名称"
'           @20181211   公式分割GA Tickets为GA Tickets为GA Tickets网站和GA TicketsM站
'           @20181212   解决保存时需要手动选择格式的问题（直接保存时透视表格式会丢失），直接在当前目录下保存为.xlsx文件
'           @20190624   删除敏感信息列（观众IP，姓名，账号，手机号，地区）操作
'注意事项：无
'====================================================================================================

Option Explicit '所有变量必须先定义才能使用
Sub AmountCheck()

    '关闭屏幕更新，以节省程序运行时间
    Application.ScreenUpdating = False


    '系统直接导出的销售报表，前3行为标题行，第5行为英文标题行，无用且影响生成透视表，所以需要先删除
    '删除后添加筛选
    Range("1:3,5:5").Select
    Selection.Delete Shift:=xlUp

    Rows("1:1").Select
    Selection.AutoFilter


    '删除敏感信息列，使用绝对引用，20190624增加
    Range("I:M,AL:AL").Select
    Selection.Delete Shift:=xlToLeft

    '==============================================================================================================================
    '定义3个变量，总行数，当前行，当前列,Inter(2个字节)的范围是-32768 -- 32767，Long(4个字节)的范围是-2147483648 -- 2147483648
    Dim totalRows, currentRow, currentColumn As Long

    '取得当前活动单元格所在区域的总行数
    totalRows = ActiveCell.CurrentRegion.Rows.count


    '==============================================================================================================================

    '添加1个空白列A，在该列第1个单元格中填充"序号"（便于后期处理时确保每行唯一性）
    ActiveSheet.Columns("A").Insert Shift:=xlToRight, CopyOrigin:=xlFormatFromLeftOrAbove

    'ActiveCell.Select
    Range("A1").Select
    ActiveCell.FormulaR1C1 = "序号"

    Range("A2").Select
    ActiveCell.FormulaR1C1 = "1"

    '取得当前行，当前列
    currentRow = ActiveCell.Row
    currentColumn = ActiveCell.Column

    Selection.AutoFill Destination:=Range(Cells(currentRow, currentColumn), Cells(totalRows, currentColumn)), Type:=xlFillDefault
    Range(Cells(currentRow, currentColumn), Cells(totalRows, currentColumn)).Select
    Selection.DataSeries Rowcol:=xlColumns, Type:=xlLinear, Date:=xlDay, _
        Step:=1, Trend:=False


    '==============================================================================================================================
    '添加1个空白列AL，在该列第1个单元格中填充"付款方式"
    ActiveSheet.Columns("AG").Insert Shift:=xlToRight, CopyOrigin:=xlFormatFromLeftOrAbove
    Range("AG1").Select
    ActiveCell.FormulaR1C1 = "付款方式"

    '==============================================================================================================================
    'Count total rows, then auto fill the column from AK2 to end with Pay Type
    '统计全部有效行，然后从AL2开始，自动填充支付类型计算公式

    '选中AG2单元格
    Range("AG2").Select

    '填充支付类型计算公式，使用了相对引用R[]C[]
    '主题公式：IF(logical_test,value_if_ture,value_if_false)
    '需要特别注意，此处因为等号右边为函数，字符串加两个引号

    '第1步，
        'FIND(字符，字符串),返回"字符"在"字符串"中的位置，不区分大小写。如果找不到，返回#VALUE!(值错误)
        'FIND("*",AK2),在AK2单元格中搜索*号，得到*号在第几个字符
    '第2步，IF(ISERROR(FIND(""*"",AK2)-1),0,FIND(""*"",AK2)-1))
        'ISERROR(value) 判断是否值错误
        '如果找不到，IF表达式的值为0，
        '如果找到，IF表达式的值就是*的实际位置
    '第3步，LEFT(AK2,第二步结果)
        '如果找不到*，得到0
        '如果找到*，则返回*号前面的全部字符
    '第4步,在AI2中搜索"|",IF(ISERROR(FIND(""|"",AK2)),第3步结果,""扫码以及云支付""))"
        '如果找到，则IF表达式的值为 "扫码以及云支付"
        '如果找不到，则IF表达式的值为第3步结果
    '第5步
        '如果I2 等于这6个字符串（渠道）中的1个，并且第4步的值 = 银联支付，两个条件同时满足，则支付方式 = 通联支付
        '否则支付方式 =  第4步的值

    '第6步
        '如果结果等于GA Tickets，那么就取对应的I列（渠道）单元格内“网站销售渠道”或者“M站销售渠道”的前两个字符，拼接成最后的方式
        '

'    Dim str As String
'
'    str = "=IF(AND(OR(RC[-29]=""Box Office"",RC[-29]=""DSA"",RC[-29]=""Club 33"",RC[-29]=""DG"",RC[-29]=""Hotel 1"",RC[-29]=""Hotel 2"")," & _
'            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")=""银联支付""),""通联支付""," & _
'            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付""))"


    'RC[-24] 代表相对引用，从当前列向左数到24
    ActiveCell.FormulaR1C1 = _
    "=IF( IF(AND(OR(RC[-24]=""Box Office"",RC[-24]=""DSA"",RC[-24]=""Club 33"",RC[-24]=""DG"",RC[-24]=""Hotel 1"",RC[-24]=""Hotel 2"")," & _
            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")=""银联支付""),""通联支付""," & _
            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付""))=""GA Tickets"",""GA Tickets""&LEFT(RC[-24],2), IF(AND(OR(RC[-24]=""Box Office"",RC[-24]=""DSA"",RC[-24]=""Club 33"",RC[-24]=""DG"",RC[-24]=""Hotel 1"",RC[-24]=""Hotel 2"")," & _
            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")=""银联支付""),""通联支付""," & _
            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")))"


'    ActiveCell.FormulaR1C1 = _
'    "=IF( IF(AND(OR(RC[-29]=""Box Office"",RC[-29]=""DSA"",RC[-29]=""Club 33"",RC[-29]=""DG"",RC[-29]=""Hotel 1"",RC[-29]=""Hotel 2"")," & _
'            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")=""银联支付""),""通联支付""," & _
'            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付""))=""GA Tickets"",""GA Tickets""&LEFT(RC[-29],2), IF(AND(OR(RC[-29]=""Box Office"",RC[-29]=""DSA"",RC[-29]=""Club 33"",RC[-29]=""DG"",RC[-29]=""Hotel 1"",RC[-29]=""Hotel 2"")," & _
'            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")=""银联支付""),""通联支付""," & _
'            "IF(ISERROR(FIND(""|"",RC[-1])),LEFT(RC[-1],IF(ISERROR(FIND(""*"",RC[-1])-1),0,FIND(""*"",RC[-1])-1)),""扫码以及云支付"")))"


    '重新取得当前行，当前列
    currentRow = ActiveCell.Row
    currentColumn = ActiveCell.Column

    'Range(起始单元格，结束单元格)
    '在当前列选中的区域自动填充公式
    Selection.AutoFill Destination:=Range(Cells(currentRow, currentColumn), Cells(totalRows, currentColumn))


    '==============================================================================================================================
    '定义变量,并赋值为当前sheet的名称
    Dim srcSheetName As String
    srcSheetName = ActiveSheet.Name

    '==============================================================================================================================
    '在sheet1生成第1个透视表，行区域为"渠道",值区域为"总价"，汇总方式为"求和"
    '选中活动的sheet
    ActiveSheet.Select

    '在活动sheet之前添加新的sheet
    Sheets.Add

    '生成数据透视表，参数默认
    ActiveWorkbook.PivotCaches.Create(SourceType:=xlDatabase, SourceData:= _
        Sheets(srcSheetName).Range("A1").CurrentRegion, Version:=xlPivotTableVersion10). _
        CreatePivotTable TableDestination:="Sheet1!R3C1", TableName:="数据透视表1", _
        DefaultVersion:=xlPivotTableVersion10

    '选中新生成的sheet1
    Sheets("Sheet1").Select

    '选中单元格(3,1)
    Cells(3, 1).Select


    With ActiveSheet.PivotTables("数据透视表1")
        '将"渠道" 添加至透视表行区域
        .PivotFields("渠道").Orientation = xlRowField
        .PivotFields("渠道").Position = 1


        '将"项目名称"添加进"筛选器"区域(xlPageFiled),此时默认的 Page = "全部"
        .PivotFields("项目名称").Orientation = xlPageField
        .PivotFields("项目名称").Position = 1

        '将"总价" 添加至透视表的值区域，并自定义名称："求和项:总价"，以及设置值汇总方式"求和"(xlSum)
        .AddDataField ActiveSheet.PivotTables("数据透视表1").PivotFields("总价"), "求和项:总价", xlSum
    End With


    '==============================================================================================================================
    '在sheet2生成第2个透视表，行区域为"付款方式",值区域为"总价"，汇总方式为"求和"
    '选中当前活动sheet（Sheet1）
    ActiveSheet.Select

    '在sheet1前添加新的sheet
    Sheets.Add

    '在数据透视表1的基础上，生成透视表2
    ActiveWorkbook.Worksheets("Sheet1").PivotTables("数据透视表1").PivotCache. _
        CreatePivotTable TableDestination:="Sheet2!R3C1", TableName:="数据透视表2", _
        DefaultVersion:=xlPivotTableVersion10

    '选中Sheet2
    Sheets("Sheet2").Select

    '选中单元格（3，1）
    Cells(3, 1).Select


    With ActiveSheet.PivotTables("数据透视表2")
        '将"付款方式" 添加到行区域
        .PivotFields("付款方式").Orientation = xlRowField
        .PivotFields("付款方式").Position = 1

        '将"项目名称"添加进"筛选器"区域(xlPageFiled),此时默认的 Page = "全部"
        .PivotFields("项目名称").Orientation = xlPageField
        .PivotFields("项目名称").Position = 1

        '将"总价"添加到值区域，并修改值字段汇总方式为"求和"，默认方式是"计数"(xlCount)
        .AddDataField ActiveSheet.PivotTables("数据透视表2").PivotFields("总价"), "求和项:总价", xlSum
    End With


    '==============================================================================================================================
    '在sheet3生成第3个透视表，行区域为"总价",值区域为"总价"，汇总方式为"计数"，筛选器为"支付宝"
    '选中活动的Sheet
    ActiveSheet.Select

    '添加新的Sheet，即为sheet3
    Sheets.Add

    '在数据透视表1 基础上生成透视表3
    ActiveWorkbook.Worksheets("Sheet1").PivotTables("数据透视表1").PivotCache. _
        CreatePivotTable TableDestination:="Sheet3!R3C1", TableName:="数据透视表3", _
        DefaultVersion:=xlPivotTableVersion10

    '选中sheet3中的单元格(3,1)
    Sheets("Sheet3").Select
    Cells(3, 1).Select


    With ActiveSheet.PivotTables("数据透视表3")
        '将"总价"添加进值区域
        .AddDataField ActiveSheet.PivotTables("数据透视表3").PivotFields("总价"), "计数项:总价", xlCount

        '将"项目名称"添加进"筛选器"区域(xlPageFiled),此时默认的 Page = "全部"
        .PivotFields("项目名称").Orientation = xlPageField
        .PivotFields("项目名称").Position = 1

        '将"付款方式"添加进筛选器区域(xlPageFiled)
        .PivotFields("付款方式").Orientation = xlPageField
        .PivotFields("付款方式").Position = 1

        '将"总价"添加进行区域
        .PivotFields("总价").Orientation = xlRowField
        .PivotFields("总价").Position = 1
    End With



    '遍历全部支付方式，如果"支付宝"存在，则将过滤器值设为"支付宝"，否则为默认的全部
    Dim pfPage As PivotItem
    For Each pfPage In ActiveSheet.PivotTables("数据透视表3").PivotFields("付款方式").PivotItems
        If pfPage = "支付宝" Then
            '将筛选器中的"付款港式"值设为"支付宝"
            ActiveSheet.PivotTables("数据透视表3").PivotFields("付款方式").CurrentPage = "支付宝"

            Exit For
        End If
    Next

    '==============================================================================================================================
    'sheet4 生成现金支付订单透视表，sheet5生成退单透视表
    '在sheet4生成第4个透视表，行区域为"序号"，"订单号",值区域为"总价"，汇总方式为"求和"，筛选器为"现金"
    '选中活动的Sheet
    ActiveSheet.Select

    '添加新的Sheet，即为sheet4
    Sheets.Add

    '在数据透视表1 基础上生成透视表4
    ActiveWorkbook.Worksheets("Sheet1").PivotTables("数据透视表1").PivotCache. _
        CreatePivotTable TableDestination:="Sheet4!R3C1", TableName:="数据透视表4", _
        DefaultVersion:=xlPivotTableVersion10

    '选中sheet4中的单元格(3,1)
    Sheets("Sheet4").Select
    Cells(3, 1).Select


    With ActiveSheet.PivotTables("数据透视表4")
        '将"总价"添加进"值"区域,汇总方式为"求和"
        .AddDataField ActiveSheet.PivotTables("数据透视表4").PivotFields("总价"), "计数项:总价", xlSum

        '将"项目名称"添加进"筛选器"区域(xlPageFiled),此时默认的 Page = "全部"
        .PivotFields("项目名称").Orientation = xlPageField
        .PivotFields("项目名称").Position = 1

        '将"付款方式"添加进"筛选器"区域(xlPageFiled),此时默认的 Page = "全部"
        .PivotFields("付款方式").Orientation = xlPageField
        .PivotFields("付款方式").Position = 1
    End With



    '遍历全部支付方式，如果"现金"存在，则将过滤器值设为"现金"，否则为默认的全部
    For Each pfPage In ActiveSheet.PivotTables("数据透视表4").PivotFields("付款方式").PivotItems
        If pfPage = "现金" Then


            ActiveSheet.PivotTables ("数据透视表4")


            With ActiveSheet.PivotTables("数据透视表4")
                '将筛选器中的"付款港式"值设为"现金"
                .PivotFields("付款方式").CurrentPage = "现金"

                '将"序号"添加进"行"区域
                .PivotFields("序号").Orientation = xlRowField
                .PivotFields("序号").Position = 1

                '将"订单号"添加进"行"区域
                .PivotFields("订单号").Orientation = xlRowField
                .PivotFields("订单号").Position = 2

                '对"行"和"列"禁用总计
                .ColumnGrand = False
                .RowGrand = False

                '不显示分类汇总
                .PivotFields("序号").Subtotals = Array(False, False, False, False, False, False, False, False, False, False, False, False)
            End With

            Exit For
        End If
    Next
    '==============================================================================================================================
    '在sheet5生成第5个透视表，行区域为"关联凭证",值区域为"总价"，汇总方式为"求和"，筛选器为"付款方式"
    '选中活动的Sheet
    ActiveSheet.Select

    '添加新的Sheet，即为sheet5
    Sheets.Add

    '在数据透视表1 基础上生成透视表5
    ActiveWorkbook.Worksheets("Sheet1").PivotTables("数据透视表1").PivotCache. _
        CreatePivotTable TableDestination:="Sheet5!R3C1", TableName:="数据透视表5", _
        DefaultVersion:=xlPivotTableVersion10

    '选中sheet5中的单元格(3,1)
    Sheets("Sheet5").Select
    Cells(3, 1).Select


    With ActiveSheet.PivotTables("数据透视表5")
        '将"总价"添加进值区域，汇总方式为"求和"
        .AddDataField ActiveSheet.PivotTables("数据透视表5").PivotFields("总价"), "计数项:总价", xlSum

        '将"项目名称"添加进"筛选器"区域(xlPageFiled),此时默认的 Page = "全部"
        .PivotFields("项目名称").Orientation = xlPageField
        .PivotFields("项目名称").Position = 1

        '将"付款方式"添加进筛选器区域(xlPageFiled)
        .PivotFields("付款方式").Orientation = xlPageField
        .PivotFields("付款方式").Position = 1

        '将"关联凭证"添加进行区域
        .PivotFields("关联凭证").Orientation = xlRowField
        .PivotFields("关联凭证").Position = 1

        '对"行"和"列"禁用总计
        .ColumnGrand = False
        .RowGrand = False

        '不显示分类汇总
        .PivotFields("关联凭证").Subtotals = Array(False, False, False, False, False, False, False, False, False, False, False, False)
    End With


    '遍历全部支付方式，如果""（表示退款）存在，则将过滤器值设为""，否则为默认的全部
    For Each pfPage In ActiveSheet.PivotTables("数据透视表5").PivotFields("付款方式").PivotItems
        If pfPage = "" Then
            '将筛选器中的"付款港式"值设为""
            ActiveSheet.PivotTables("数据透视表5").PivotFields("付款方式").CurrentPage = ""

            Exit For
        End If
    Next
    '==============================================================================================================================
    '在当前活动Sheet前面，添加新的Sheet,即为sheet6
    Sheets.Add Before:=ActiveSheet

    '选中Sheet2
    Sheets("Sheet2").Select
    Sheets("Sheet2").UsedRange.Select

    '选中A3单元格所在的活动区域
    'Range("A3").CurrentRegion.Select

    '复制并粘贴该区域
    Selection.Copy Sheets("Sheet6").Range("A1")

    '选中Sheet1
    Sheets("Sheet1").Select
    Sheets("Sheet1").UsedRange.Select

    '选中A3所在的活动区域
    'Range("A3").CurrentRegion.Select

    '复制并粘贴该区域
    'Application.CutCopyMode = False
    Selection.Copy Sheets("Sheet6").Range("D1")

    '回到Sheet6
    Sheets("Sheet6").Select


    '重命名刚才生成的6个sheet
'    Sheets("Sheet1").Name = "渠道-总价-求和"
'    Sheets("Sheet2").Name = "付款方式-总价-求和"
'    Sheets("Sheet3").Name = "付款方式-总价-计数"
'    Sheets("Sheet4").Name = "付款方式-现金-订单号"
'    Sheets("Sheet5").Name = "退款-关联凭证"
'    Sheets("Sheet6").Name = "透视表汇总"

    '设置表格列宽为自适应
    Columns.EntireColumn.AutoFit

    '恢复屏幕更新
    Application.ScreenUpdating = False

    '====================================================================================================================
    '保存文件
    Dim newFileName As String

    'InStrRev 函数：返回参数2在参数1的出现的位置
    newFileName = Left(ActiveWorkbook.FullName, InStrRev(ActiveWorkbook.FullName, ".")) & "xlsx"

    'Application.DisplayAlerts = False

    ActiveWorkbook.SaveAs Filename:=newFileName, FileFormat:=xlOpenXMLWorkbook

    'Application.DisplayAlerts = True
    '====================================================================================================================

End Sub