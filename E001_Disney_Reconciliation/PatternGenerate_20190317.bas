
Attribute VB_Name = "PatternGenerate"
'================================================================================================================
'创建日期:  @20180813
'文件描述:  生成模板
'修改记录:  @20181107:  增加支付方式"扫码以及云支付"
'                       在"小计"列增加求和公式
'           @20181110:  所有变量都指定类型
'                       日期变更改用DateAdd()函数，上月最后1天加1后，自动变为下月第1天
'           @20181209   增加对ScreenUpdating属性的设置，以节约程序运行时间
'================================================================================================================
Option Explicit

'声明全局变量,timesFlag(次数标志)用来控制总行数
Public timesFlag As Byte
'================================================================================================================
'名称:  FormatGenerate
'描述:  分两步生成模板，第一步判断是否生成"支付方式"行，并执行
'                       第二步生成其他的"统计方式"字段，并填充公式
'参数:  无
'================================================================================================================
Sub FormatGenerate()

    '关闭屏幕更新，以节省程序运行时间
    Application.ScreenUpdating = False

    '初始化全局变量
    timesFlag = 0

    '选中单元格A1
    Range("A1").Select

    '如果单元格A1的值 不等于 "日期"，则该Excel表为新的空白表格
    If (ActiveCell.Value <> "日期") Then

        'Not timesFlag，对timesFlag取反，这样FirstTime函数只是在空白Excel中才会被调用
        If (Not timesFlag) Then
            FirstTime
        End If

    '如果单元格A1的值 等于 "日期"
    Else
        timesFlag = 1
        NotTheFirstTime
    End If

    '恢复屏幕更新
    Application.ScreenUpdating = False

End Sub
'================================================================================================================
'名称:  FirstTime
'描述:  在空白Excel执行本宏时，该函数会被调用，用来生成第一行"支付方式"
'参数:  无
'================================================================================================================
Sub FirstTime()

    '选中A1 单元格
    Range("A1").Select

    '将指定的支付方式逐个填充第1行的单元格
    ActiveCell.Value = "日期"
    ActiveCell.Offset(0, 1).Range("A1").Value = "类别"
    ActiveCell.Offset(0, 2).Range("A1").Value = "支付宝"
    ActiveCell.Offset(0, 3).Range("A1").Value = "微信"
    ActiveCell.Offset(0, 4).Range("A1").Value = "银联"
    ActiveCell.Offset(0, 5).Range("A1").Value = "通联"
    ActiveCell.Offset(0, 6).Range("A1").Value = "扫码以及云支付"
    ActiveCell.Offset(0, 7).Range("A1").Value = "payeco内卡"
    ActiveCell.Offset(0, 8).Range("A1").Value = "渠道应收"
    ActiveCell.Offset(0, 9).Range("A1").Value = "小计"

    '选中被填充的单元格(A1:J1),设置字体为"粗体"
    ActiveCell.Range("A1:J1").Select
    Selection.Font.Bold = True

    'Request a date input
    '选中A2单元格，弹出输入框，要求按照yyyymmdd格式输入日期,默认值为用Date函数获取的当天日期
    ActiveCell.Offset(1, 0).Range("A1").Select
    ActiveCell.Value = Application.InputBox(Prompt:="请按照 YYYY/MM/DD 格式输入日期：", _
                                            Title:="Input", _
                                            Default:=Format(Date, "General Date"), _
                                            Type:=2)
    '调用函数，生成剩余的填充格式
    NotTheFirstTime
End Sub
'================================================================================================================
'名称:  NotTheFirstTime
'描述:  生成"列"填充内容，设置单元格格式，填充公式
'参数:  无
'================================================================================================================
Sub NotTheFirstTime()

    '定义变量：总行数，当前行，当前列
    Dim totalRows, currentRow, currentColumn As Integer

    '总行数 = 活动区域的行数 + timesFlag
    '在空白Excel第1次使用 和 在非空白Excel使用 得到的值不同
    '第1次使用时：totalRows = 2 + 0
    '非第一次使用时：totalRows = 1（第1行） + 5N（中间填充的5行） + 1
    '加timesFlag 是为了从当前表格区域的下一行开始
    totalRows = ActiveCell.CurrentRegion.Rows.count + timesFlag

    '如果本宏是第1次运行(空白Excel)，则跳过这段代码
    '如果本宏不是第1次运行（非空白Excel），则执行下面代码，根据向上偏移5个单元格，内容自动填充日期
    If timesFlag Then
        Cells(totalRows, 1).Select
        Dim preDateVal As Date

        '两个备用函数(w3school)
        'IsDate(Expression):可用来判断 Expression 是否可被转换为日期或时间
        'CDate(Expression)：把一个合法的日期和时间表达式转换为 Date 类型
        preDateVal = ActiveCell.Offset(-5, 0).Value
        ActiveCell.Value = DateAdd("d", 1, preDateVal)
    End If


    '填充列
    ActiveCell.Offset(0, 1).Range("A1").Value = "系统记录应收"
    ActiveCell.Offset(1, 1).Range("A1").Value = "财务实收"
    ActiveCell.Offset(2, 1).Range("A1").Value = "手续费"
    ActiveCell.Offset(3, 1).Range("A1").Value = "调账"
    ActiveCell.Offset(4, 1).Range("A1").Value = "ck"

    '选中A1所在的活动区域
    Range("A1").CurrentRegion.Select

    '====================================================================================================
    '设置边框
    Selection.Borders(xlDiagonalDown).LineStyle = xlNone
    Selection.Borders(xlDiagonalUp).LineStyle = xlNone

    Selection.Borders(xlEdgeLeft).LineStyle = xlContinuous
    Selection.Borders(xlEdgeLeft).Weight = xlThin

    Selection.Borders(xlEdgeTop).LineStyle = xlContinuous
    Selection.Borders(xlEdgeTop).Weight = xlThin

    Selection.Borders(xlEdgeBottom).LineStyle = xlContinuous
    Selection.Borders(xlEdgeBottom).Weight = xlThin

    Selection.Borders(xlEdgeRight).LineStyle = xlContinuous
    Selection.Borders(xlEdgeRight).Weight = xlThin

    Selection.Borders(xlInsideVertical).LineStyle = xlContinuous
    Selection.Borders(xlInsideVertical).Weight = xlThin

    Selection.Borders(xlInsideHorizontal).LineStyle = xlContinuous
    Selection.Borders(xlInsideHorizontal).Weight = xlThin

    '设置对齐方式
    Selection.HorizontalAlignment = xlCenter


    '====================================================================================================
    '需要重新选中单元格，因为上一步的操作选中的是整个区域"CurrentRegion.Select"
    Cells(totalRows, 1).Select

    '向右移动两个单元格，并以新的单元格为基准，选中单元格区域(A1:H5),单元格使用了相对引用
    ActiveCell.Offset(0, 2).Range("A1:H5").Select

    '设置单元格格式
    Selection.NumberFormatLocal = "￥#,##0.00;￥-#,##0.00"

    '以当前单元格为基准向下移动4个单元格，并选中
    ActiveCell.Offset(4, 0).Range("A1").Select

    '填充公式
    ActiveCell.FormulaR1C1 = "=R[-2]C+R[-3]C-R[-4]C"

    '选中活动单元格
    ActiveCell.Select

    '在A1到G1区域自动填充公式
    Selection.AutoFill Destination:=ActiveCell.Range("A1:G1"), Type:= _
        xlFillDefault

    '====================================================================================================
    '需要重新选中单元格，因为上一步的操作选中的是整个区域"CurrentRegion.Select"
    Cells(totalRows, 1).Select

    '选中同一行位于"小计"列的单元格
    ActiveCell.Offset(0, 9).Range("A1").Select

    '填充求和公式
    ActiveCell.FormulaR1C1 = "=SUM(RC[-7]:RC[-1])"

    '选中活动单元格
    ActiveCell.Select

    '在活动单元格的A1到A5范围自动填充公式
    Selection.AutoFill Destination:=ActiveCell.Range("A1:A5")

    '====================================================================================================
    '设置表格列宽为自适应
    Columns.EntireColumn.AutoFit

    '回到单元格，这一步是为使用者连续生成多个日期的填充内容时所用
    Cells(totalRows, 1).Select

End Sub

