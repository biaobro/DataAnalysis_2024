
Attribute VB_Name = "PayTypeValueFill"
'======================================================================================================================
'创建日期:  @20180813
'文件描述:  在销售报表中查找渠道对应的金额并填充进相应日记账表格中。
'修改记录:   @20181107：    增加支付方式"扫码以及云支付"
'                           改变了通知方式：只有出错时才会有通知，并将通知内容修改为中文
'                           不再使用variant型变量，占用字符空间较多：Long-4个字节，Boolean-2个字节
'           @20181209   增加对ScreenUpdating属性的设置，以节约程序运行时间
'           @20181224   增加对Sheet6 的重新选择
'使用说明： 必须选中需要填充金额部分对应的日期单元格，然后执行该宏
'======================================================================================================================

Option Explicit
Public errStatus As Boolean     'error status
Public wkb As Workbook          'public variant
Public targetFile As String       'public variant
Public fileStatus As Integer
Public srcFile As String
'================================================================================================================
'名称:  PayTypeValueFill
'描述:  打开名称中所含日期匹配的销售表，并将支付方式对应的金额填充到相应的单元格中
'参数:  无
'================================================================================================================
Sub PayTypeValueFill()

    '关闭屏幕更新，以节省程序运行时间
    Application.ScreenUpdating = False

    '初始化状态变量
        'fileStatus = 0 表示文件未打开
        'errStatus = 0 表示没有错误
    fileStatus = 0
    errStatus = 0

    srcFile = ActiveWorkbook.Name

    '显示1个对话框，引导使用者选择正确的文件
    SelectFile

    '文件选择正确，执行If中的语句
    '文件选择错误，则直接跳出，不做任何进一步动作
    If errStatus Then
        SearchThenFill
    End If

    '恢复屏幕更新
    Application.ScreenUpdating = False
End Sub
'=================================================================================================================
'名称：SelectFile
'描述: 选择单一文件，在背后（非后台）打开,将其设为活动Workbook，统计其中sheet的数量
'参数：无
'=================================================================================================================
Sub SelectFile()
    With Application.FileDialog(msoFileDialogFilePicker)
        '禁止选择多个文件
        .AllowMultiSelect = False

        '清空过滤器
        .Filters.Clear

        '设置Excel文件对应的后缀名过滤器
        .Filters.Add "Excel Files", "*.xls;*.xlsx"

        '如果对话框成功显示
        If .Show = -1 Then

            '获取单元格的值，并转换格式为yyyymmdd，原格式为2018/11/10,会影响接下来的比较
            Dim dateValue As String
            dateValue = Format(ActiveCell.Value, "yyyymmdd")

            '获取被选中文件的文件名
            targetFile = .SelectedItems(1)

            '文件名包含路径，将其去掉，只保留名称
            targetFile = Right(targetFile, Len(targetFile) - InStrRev(targetFile, "\"))

            '检查该文件文件名是否与所选日期匹配
            If .SelectedItems(1) Like "*" & dateValue & "*" Then

                '文件选择正确
                errStatus = 1

                '=================================================================================================================
                '检查被选中的文件是否已经处于被打开状态
                Dim count As Integer

                '获取当前系统中全部打开的Workbook数量
                count = Workbooks.count

                Dim i As Byte

                '逐个比较Workbook的名称是否与被选中文件名相同，如果相同，则fileStatus 置为1，表示该文件已经打开，后续不需要执行打开操作
                For i = 1 To count Step 1
                    If Workbooks(i).Name = targetFile Then
                        fileStatus = 1
                    End If
                Next

                '如果没有找到，说明文件未被打开，那么打开这个选中的文件
                If fileStatus = 0 Then
                    Workbooks.Open (targetFile)
                End If

                '激活打开的文件，这一步是否必要？
                Workbooks(targetFile).Activate

                '激活（选中）Sheet6，因为相关值需要从Sheet6取得
                '上一步MaizuoOrderDetails保存时已经选择Sheet6，但不排除中间修改的可能
                '以防万一还是加上选择Sheet6的这个动作
                Sheets("Sheet6").Select
                '=================================================================================================================

            '如果被选中文件的名称与日期值不匹配， 则弹出警告框，并将错误状态值置为0
            Else
                errStatus = 0
                MsgBox "错误, 请选择日期匹配的文件!!!", vbExclamation + vbOKOnly
            End If
        End If

    End With
End Sub
'=================================================================================================================
'名称：SearchThenFill
'描述: 选择单一文件，在背后（非后台）打开,将其设为活动Workbook，统计其中sheet的数量
'参数：无
'=================================================================================================================
Sub SearchThenFill()

    '定义变量，并初始化
    Dim rngSrc As Range

    '定义支付方式数组
    Dim payType(7) As String

    payType(0) = "支付宝"
    payType(1) = "微信"
    payType(2) = "银联支付"
    payType(3) = "通联支付"
    payType(4) = "扫码以及云支付"
    payType(5) = "payeco内卡"
    payType(6) = "应收账款"

    '定义支付方式金额数组
    Dim payValue(7) As Long

    payValue(0) = 0
    payValue(1) = 0
    payValue(2) = 0
    payValue(3) = 0
    payValue(4) = 0
    payValue(5) = 0
    payValue(6) = 0

    '定义"未找到"变量，并初始化为空，string变量默认是可变长的variant。String * N 表示最大字符长度为N，汉字和英文字母都各算1个字符
    Dim noPayTypeFound As String
    noPayTypeFound = ""

    Dim i As Integer

    '在销售报表sheet6中搜索
    For i = 0 To 6 Step 1
        Set rngSrc = Cells.Find(payType(i))

        If rngSrc Is Nothing Then
            '如果没找到，则将该支付方式记录在字符串中
            noPayTypeFound = noPayTypeFound + "     " + payType(i) + Chr(13)
        Else
            '如果找到，则将值付给金额数组中对应的元素
            payValue(i) = rngSrc.Offset(0, 1).Value
        End If
    Next

    '如果以上支付方式未在销售表中找到，则弹出提示框，Chr(13) 表示换行
    If noPayTypeFound <> "" Then
        MsgBox "以下支付方式未找到: " & Chr(13) & noPayTypeFound & "请注意!!!"
    End If

    '关闭文件
    If fileStatus = 0 Then
        Workbooks(targetFile).Close
    End If

    '激活源文件，日记账表格.
    '如果不执行这个步骤，并有多个Workbook被打开的时候，就会报错
    Workbooks(srcFile).Activate

    '逐个填充
    For i = 0 To 6 Step 1
        ActiveCell.Offset(0, i + 2).Range("A1").Value = payValue(i)
    Next

    '调整列宽为自适应，完整显示全部金额
    Columns.EntireColumn.AutoFit
End Sub


