Option Explicit


Sub Macro()
'
' Macro1 宏
'

'   '声明定时器
    Dim startTime As Single

    '声明计数器
    Dim i As Integer

    '声明源文件名称
    Dim srcFile As String

    '声明源文件总行数
    Dim rowCount As Long

    '声明源工作簿，工作表
    Dim srcWorkbook As Workbook
    Dim srcWorksheet As Worksheet

    '声明行复制区域的起始位置，Integer范围有限，所以改用Long
    Dim rowStart, rowStop As Long
    rowStart = 0
    rowStop = 0

    '声明将要生成的文件数量
    Dim fileCount As Integer

    '声明新生成的文件容纳行数
    Dim rowPerFile As Long
    rowPerFile = 10000

    '声明新生成的文件名
    Dim newFileName As String
    newFileName = ""

    '声明新生成的工作簿，工作表
    Dim destWorkbook As Workbook
    Dim destSheet As Worksheet

    '弹出文件选择框
    With Application.FileDialog(msoFileDialogFilePicker)
        '禁止选择多个文件
        .AllowMultiSelect = False

        '清空过滤器
        .Filters.Clear

        '设置Excel文件对应的后缀名过滤器
        .Filters.Add "Excel Files", "*.xls;*.xlsx"

        '如果对话框成功显示
        If .Show = -1 Then

            '获取被选中文件的文件名
            srcFile = .SelectedItems(1)

            '调试打印，确认选择的文件
            Debug.Print ("srcFile : " & srcFile)
        Else
            srcFile = ""
        End If
    End With

    '如果没有选择文件，则退出
    If (srcFile = "") Then
        Exit Sub
    End If

    '新启动1个App,在新App中，打开源文件，并设为不可见，后台打开
    Dim newApp As Excel.Application
    Set newApp = CreateObject("Excel.Application")
    newApp.Visible = False
    Set srcWorkbook = newApp.Workbooks.Open(srcFile)
    Set srcWorksheet = srcWorkbook.Worksheets(1)

    '关闭屏幕更新，以节省程序运行时间
    Application.ScreenUpdating = False

    '获取启动时间
    startTime = Timer

    '获取源文件行数
    rowCount = srcWorksheet.Cells(1, 1).CurrentRegion.Rows.count

    '确定将要生成的文件数量
    If (rowCount Mod rowPerFile) <> 0 Then
        fileCount = rowCount \ rowPerFile + 1
    Else
        fileCount = rowCount \ rowPerFile
    End If

    '调试打印
    'Debug.Print ("rowCount : " & rowCount)
    'Debug.Print ("fileCount : " & fileCount)

    '弹出对话框，如取消，则不再往下执行
    If ((MsgBox("共有 " & rowCount - 1 & " 行数据，将生成 " & fileCount & " 个文件，请确认。", vbOKCancel) = vbCancel)) Then
        Exit Sub
    End If


    '开始循环处理
    For i = 1 To fileCount
        '新文件的全称，含保存路径
        newFileName = srcWorkbook.Path & "\AfterProcess_" & i & ".xlsx"

        '复制第一行
        srcWorksheet.Rows(1).Copy

        '生成新的工作簿
        Set destWorkbook = Workbooks.Add

        '粘贴第一行
        ActiveSheet.Paste

        '退出复制粘贴模式
        newApp.CutCopyMode = False

        '从复制复制1万行数据
        rowStart = (i - 1) * rowPerFile + 2
        rowStop = i * rowPerFile + 1
        srcWorksheet.Range(srcWorksheet.Cells(rowStart, 1), srcWorksheet.Cells(rowStop, 18)).Copy

        '激活新生成的工作簿
        Workbooks(destWorkbook.Name).Activate

        '以A2为左上角进行粘贴
        Range("A2").Select
        ActiveSheet.Paste

        '退出复制粘贴模式
        newApp.CutCopyMode = False

        '填充备注列
        Range(Cells(2, 11), Cells(rowPerFile + 1, 11)) = Format(Date, "yyyymmdd") & "-会员导入-" & Format(i, "00")
        Range("A1").Select

        '清除格式
        ActiveSheet.Cells.ClearFormats

        '保存并关闭
        ActiveWorkbook.SaveAs Filename:=newFileName, FileFormat:=xlOpenXMLWorkbook
        ActiveWorkbook.Close

    Next i

    newApp.Quit
    Set newApp = Nothing
    Set srcWorkbook = Nothing

    '恢复屏幕更新
    Application.ScreenUpdating = False

    'Debug.Print ((Timer - startTime) * 1000 & " ms")
    MsgBox ("处理完成，用时" & (Timer - startTime) * 1000 & " ms")
End Sub