
Attribute VB_Name = "PayChannelValueFill"
'=========================================================================================================================================================
'创建日期:  @20180813
'文件描述:  @
'修改记录： @20181110   改用VB自带的格式化函数Format，弃用Application.WorksheetFunction.Text
'           @20181120   增加两个分销渠道Yuanjing和Klook；增加付款方式GA Tickets
'           @20181121   增加函数，确认现金支付的订单中是否有退款，如有，需要扣除
'           @20181123   更新程序逻辑，如果现金金额不为0，才执行函数cashValueConfirm
'           @20181126   M站收款金额中需要扣除GA Tickets的收款值
'           @20181209   增加对ScreenUpdating属性的设置，以节约程序运行时间
'           @20181211   分割GA Tickets为GA Tickets为GA Tickets网站和GA TicketsM站
'           @20181212   因为迪士尼增加了项目，“美女与野兽”“星愿滑冰场”，需要填写两个Weekly Reconciliaiton Report,所以在SelectFile
'                      函数中增加了对文件名的判断，并相应设置目标文件透视表筛选器中的项目名称
'           @20181217   增加了对数组空数值的判断，如果数值为空，就不进行运算。（因为数组初始化为字符型，不能和数值直接运算，初始化为字符是为了当数据为0时，在单元格能显示为空
'                       增加对数据透视表1，项目名称的设定
'                       去掉关闭"日销售报表时"提示保存的提示
'                       增加支付渠道"HuiXiang"
'           @20181224   错误修正。现金退款函数修正，因为筛选器增加，所以凭证区域需要响应下移至从A4开始。
'                       修正
'           @20190317   增加支付渠道"Qunar"
'           @20190521   付款类型为负数，付款方式不为空时，不需要处理；
'                       付款类型为负数，付款方式为空时，需要判断原始订单的支付方式，如果原始订单支付方式为现金或Payeco外卡，则该负数值需要填在“其他调整项”
'                       增加渠道：Motianlun
'========================================================================================================================================================
Option Explicit
Public errStatus As Integer     'error status
Public wkb As Workbook          'public variant
Public targetFile As String       'public variant
Public fileStatus As Integer
Public srcFile As String
'======================================================================
'名称：PayChannelValueFill()
'描述：搜索渠道支付金额，并填充
'参数：无
'======================================================================
Sub PayChannelValueFill()

    '关闭屏幕更新，以节省程序运行时间
    Application.ScreenUpdating = False

    '初始化变量：error status 和 file status
    '0 对应没有错误 和 文件未打开
    fileStatus = 0
    errStatus = 0

    srcFile = ActiveWorkbook.Name

    '显示对话框，并引导用户选择正确的（日期匹配）文件
    SelectFile

    '如果文件打开成功，则执行搜索并填充
    If errStatus Then
        SearchThenFill
    End If

    '恢复屏幕更新
    Application.ScreenUpdating = False

End Sub
'=======================================================================================
'名称：SelectFile()
'描述：选择单个文件，在后台打开并激活，统计sheet数量
'参数：无
'=======================================================================================
Sub SelectFile()
    With Application.FileDialog(msoFileDialogFilePicker)
        '不允许选择多个文件
        .AllowMultiSelect = False

        '设置文件类型过滤器为空
        .Filters.Clear

        '设置文件类型过滤器为"Excel Files", "*.xls;*.xlsx"
        '因为在MaizuoOrderDetails文件中已经将文件直接保存成.xlsx,所以这里去掉了*.xls,20181212修改
        '.Filters.Add "Excel Files", "*.xls;*.xlsx"
        .Filters.Add "Excel Files", "*.xlsx"


        If .Show = -1 Then
            Dim dateValue As String

            '对账明细表中，日期格式为mm-dd，为匹配正确的"待搜索"文件，需要格式转换为yyyymmdd
            '如把08-05 转换为 20180805
            'dateValue = Application.WorksheetFunction.Text(ActiveCell.Value, "yyyymmdd")
            dateValue = Format(ActiveCell.Value, "yyyymmdd")


            targetFile = .SelectedItems(1)
            targetFile = Right(targetFile, Len(targetFile) - InStrRev(targetFile, "\"))


            '检查锁打开文件的名称是否匹配 dateValue
            '如果匹配
            If .SelectedItems(1) Like "*" & dateValue & "*" Then
                '选择了正确的文件
                errStatus = 1


                Dim count As Integer
                count = Workbooks.count

                Dim i As Integer

                '统计当前所有打开的Excel文件的数量，逐个比较他们的名称是否与选中的文件名称相同
                '如果存在，则fileStatus状态置为1，表示文件已经打开
                For i = 1 To count Step 1
                    If Workbooks(i).Name = targetFile Then
                        '文件已经是"打开"状态
                        fileStatus = 1
                    End If
                Next

                '如果不存在，则打开该文件
                If fileStatus = 0 Then
                    Workbooks.Open (targetFile)
                End If

                '激活该文件
                Workbooks(targetFile).Activate

                '激活（选中）Sheet6，因为相关值需要从Sheet6取得
                '上一步MaizuoOrderDetails保存时已经选择Sheet6，但不排除中间修改的可能
                '以防万一还是加上选择Sheet6的这个动作
                Sheets("Sheet6").Select

                '根据本文件名(Weekly Reconciliaiton Report)，设置目标文件Sheet6中透视表，筛选器的内容（项目）,默认是全部 (All)
                '注意透视表在这里是 数据透视表1 和 数据透视表2
                If srcFile Like "*" & "BATB" & "*" Then
                    ActiveSheet.PivotTables("数据透视表1").PivotFields("项目名称").CurrentPage = "美女与野兽"
                    ActiveSheet.PivotTables("数据透视表2").PivotFields("项目名称").CurrentPage = "美女与野兽"
                ElseIf srcFile Like "*" & "Ice Rink" & "*" Then
                    ActiveSheet.PivotTables("数据透视表1").PivotFields("项目名称").CurrentPage = "星愿滑冰场"
                    ActiveSheet.PivotTables("数据透视表2").PivotFields("项目名称").CurrentPage = "星愿滑冰场"
                End If


            '如果不匹配，弹出警告框
            Else
                errStatus = 0
                MsgBox "错误，请选择正确的文件!!!", vbExclamation
            End If
        End If

    End With
End Sub
'=======================================================================================
'名称:SearchThenFill
'描述:从日销售报表的透视表中，
'           1.搜索各个支付渠道对应的值，并填充
'           2.搜索支付方式"payco外卡""现金"对应的值，并填充
'参数：无
'=======================================================================================
Sub SearchThenFill()

    Dim rngSrc As Range
    Dim payChannel As Variant
    Dim i As Integer

    '数组顺序必须与表格顺序一致
    '如果添加了支付渠道，请在"Fullfillment"前添加
    '20190317,增加支付渠道"Qunar"，支付渠道达到36个
    '20190521,增加支付渠道"Motianlun",支付渠道达到37个
    payChannel = Array("网站销售渠道", "M站销售渠道", "APP", "Box Office", "DSA", "Club 33", _
                         "DRC", "Hotel 1", "Hotel 2", "Ctrip", "Cooltrip", "Nanhu", "Baiyuan", _
                        "CITS", "Fenghuang", "Spring", "Shendi", "Lvmama", "Zizai", "Tuniu", _
                        "Tongcheng", "Tuzuu", "Maiqin", "Fumubang", "IPH", "Damai", "大麦直销渠道", "Maoyan", _
                        "SMG live", "Yongle", "Yuanjing", "Klook", "HuiXiang", "Qunar", "Motianlun", _
                        "Fulfillment", "DRC-Hotel Bundle")

    Dim payChannelValue As Variant

    '数组初始化为字符，是为了当数值为0的时候，显示为空
    '否则会显示为0.00
    payChannelValue = Array("", "", "", "", "", "", _
                    "", "", "", "", "", "", _
                    "", "", "", "", "", "", _
                    "", "", "", "", "", "", _
                    "", "", "", "", "", "", _
                    "", "", "", "", "", "", "")



    Dim noPayChannelFound As String
    noPayChannelFound = ""

    '共37个支付渠道
    For i = 0 To 36 Step 1
        Set rngSrc = Cells.Find(payChannel(i))

        If rngSrc Is Nothing Then
            noPayChannelFound = noPayChannelFound + "     " + payChannel(i) + Chr(13)
        Else
            payChannelValue(i) = rngSrc.Offset(0, 1).Value
        End If
    Next

    If noPayChannelFound <> "" Then
        MsgBox "以下支付方式未找到: " & Chr(13) & noPayChannelFound & "请注意!!!", vbInformation
    End If

    '=====================================================================================================
    'Dim rngSrc As Range
    Dim payType As Variant
    payType = Array("GA Tickets网站", "GA TicketsM站", "现金", "payeco外卡")

    Dim payTypeValue As Variant
    payTypeValue = Array("", "", "", "")

    Dim noPayTypeFound As String

    For i = 0 To 3 Step 1
        Set rngSrc = Cells.Find(payType(i))

        If rngSrc Is Nothing Then
            noPayTypeFound = noPayTypeFound + "     " + payType(i) + Chr(13)
        Else
            payTypeValue(i) = rngSrc.Offset(0, 1).Value
        End If
    Next

    If noPayTypeFound <> "" Then
        MsgBox "以下支付方式未找到: " & Chr(13) & noPayTypeFound & "请注意!!!"
    End If

    Dim deductionValue As Integer
    deductionValue = 0

    '如果现金值（数组第2个元素）不为0，则检查现金支付的订单中，是否存在退单情况
    If payTypeValue(2) <> "" Then
        deductionValue = returnCashValue
    End If
    '=====================================================================================================
    '关闭日销售明细表
    If fileStatus = 0 Then
        '设置退出时不保存文件
        'True表示自上次保存以来对指定工作簿不进行任何更改
        ActiveWorkbook.Saved = True

        '关闭文件
        Workbooks(targetFile).Close
    End If

    '激活需要填充内容的表格
    Workbooks(srcFile).Activate
    '=====================================================================================================
    '填充各个支付渠道对应的金额
    'ActiveCell.Offset()的参数严重依赖当前Excel结构，任何添加行的操作都需要重新调整


    '网站收款金额中需要扣除GA Tickets网站的收款值,20181211增加
    '判断网站收款金额是否为""，如果为""，则不进行扣减，20181217增加
    '相对位置第1行
    '当网站收款为0时，GA Tickets网站也一定为0
    '当网站收款不为0时，GA Tickets网站不一定为0
    If payChannelValue(0) <> "" Then
        ActiveCell.Offset(1, 0).Range("A1").Value = payChannelValue(0)

        If payTypeValue(0) <> "" Then   '如果GA Tickets网站不为空，则执行减法
            ActiveCell.Offset(1, 0).Range("A1").Value = payChannelValue(0) - payTypeValue(0)
        End If
    End If


    'M站收款金额中需要扣除GA TicketsM站的收款值,20181126增加
    '判断M站收款金额是否为""，如果为""，则不进行扣减，20181217增加
    '相对位置第2行
    '当M站收款为0时，GA TicketsM站也一定为0
    '当M站收款不为0时，GA TicketsM站不一定为0
    If payChannelValue(1) <> "" Then
        ActiveCell.Offset(2, 0).Range("A1").Value = payChannelValue(1)

        If payTypeValue(1) <> "" Then   '如果GA TicketsM站不为空，则执行减法
            ActiveCell.Offset(2, 0).Range("A1").Value = payChannelValue(1) - payTypeValue(1)
        End If
    End If


    'i 从2到8，填充剩余7个自营渠道的金额
    '相对位置从第3行到第9行
    For i = 2 To 8 Step 1
        ActiveCell.Offset(i + 1, 0).Range("A1").Value = payChannelValue(i)
    Next


    'i 从9到25，填充17个分销渠道对应的金额，
    '当分销渠道为Damai时,需要对Damai 和 大麦直销渠道 两个值求和
    '相对位置从第10行到第26行
    '因为Damai需要整合Damai和大麦直销渠道两个渠道，所以和后面的渠道处理分开
    For i = 9 To 25 Step 1
        If i = 25 Then
            If payChannelValue(i) <> "" And payChannelValue(i + 1) <> "" Then
                ActiveCell.Offset(i + 2, 0).Range("A1").Value = payChannelValue(i) + payChannelValue(i + 1)
            ElseIf payChannelValue(i) <> "" Then
                ActiveCell.Offset(i + 2, 0).Range("A1").Value = payChannelValue(i)
            ElseIf payChannelValue(i + 1) <> "" Then
                ActiveCell.Offset(i + 2, 0).Range("A1").Value = payChannelValue(i + 1)
            End If
        Else
            ActiveCell.Offset(i + 2, 0).Range("A1").Value = payChannelValue(i)
        End If
    Next

    '填充剩下的8个分销渠道金额
    '20190317,增加支付渠道"Quanr"
    '20190521,增加支付渠道"Motianlun"
    '相对位置从第28行到第35行(含)
    For i = 26 To 33 Step 1
        ActiveCell.Offset(i + 2, 0).Range("A1").Value = payChannelValue(i + 1)
    Next


    '填充 Ticketing Fullfillment
    '相对位置第40行
    ActiveCell.Offset(40, 0).Range("A1").Value = payChannelValue(35)

    '填充 Hotel Bundle Packet
    '相对位置第43行
    ActiveCell.Offset(43, 0).Range("A1").Value = payChannelValue(36)

    '=====================================================================================================
    '填入单元格"GATickets"（M站 + 网站）,相对位置第44行
    If payTypeValue(0) <> "" And payTypeValue(1) <> "" Then
        ActiveCell.Offset(44, 0).Range("A1").Value = payTypeValue(0) + payTypeValue(1)
    ElseIf payTypeValue(0) <> "" Then
        ActiveCell.Offset(44, 0).Range("A1").Value = payTypeValue(0)
    ElseIf payTypeValue(1) <> "" Then
        ActiveCell.Offset(44, 0).Range("A1").Value = payTypeValue(1)
    End If

    '填入单元格"Box Office",相对位置第52行
    ActiveCell.Offset(52, 0).Range("A1").Value = payTypeValue(2)

    '填入单元格"DRC"，相对位置第58行
    ActiveCell.Offset(58, 0).Range("A1").Value = payTypeValue(3)
    '=====================================================================================================


    '检查现金部分中是否已有订单存在退款，如有，则将退款值填充进相应区域(单元格："其他调整项"），相对位置第53行
    ActiveCell.Offset(53, 0).Range("A1").Value = deductionValue
    '=====================================================================================================

    'Columns.EntireColumn.AutoFit
End Sub
'=======================================================================================
'名称:cashValueConfirm
'描述:从日销售报表的透视表中，
'           1.搜索现金支付方式对应的值，
'           2.确认现金支付订单是否有退款记录，如有，则扣除
'参数：无
'返回值：更新后的现金支付订单总金额
'=======================================================================================
Function returnCashValue()

    Dim rngSrc As Range
    Set rngSrc = Nothing

    '设置金额初始值为0，因为最后 需要返回负数
    '用来统计现金退单金额
    Dim returnOrderAmount As Integer
    returnOrderAmount = 0

    '用来统计现金退单数量
    Dim returnOrderCount As Integer
    returnOrderCount = 0

    '回到Sheet5,"退款-关联凭证"
    Sheets("Sheet5").Select

    '选中A4所在的活动区域，单元格"计数项：总价"
    '当筛选器增加时，A4单元格也要变化
    Range("A4").CurrentRegion.Select

    '取得当前活动单元格所在区域的总行数，退单订单数量
    Dim rowCount As Integer
    rowCount = ActiveCell.CurrentRegion.Rows.count

    '回到Sheet4,"付款方式-现金-订单号",要在Sheet4中进行搜索
    Sheets("Sheet4").Select

    Dim i As Integer

    '当前实现方式是，用关联凭证，即退单对应的原始订单号，在sheet4现金支付订单号中搜索
    '-3 是因为有3行内容（标题和汇总）是无关的
    '-1 是因为i从0开始
    'Step 默认值是1，可以省略掉
    For i = 0 To (rowCount - 3 - 1) Step 1
        Set rngSrc = Cells.Find(Worksheets("Sheet5").Cells(i + 6, 1).Value)
        If rngSrc Is Nothing Then
        Else
            returnOrderCount = returnOrderCount + 1
            returnOrderAmount = returnOrderAmount - rngSrc.Offset(0, 1).Value
        End If
    Next

    MsgBox "共" & returnOrderCount & "笔现金退单！", vbInformation

    returnCashValue = returnOrderAmount

End Function

