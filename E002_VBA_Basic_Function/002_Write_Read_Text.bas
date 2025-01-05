
'Open pathname For Mode As fileName
'Write: 文本带引号
'Print: 文本不带引号，数字多空格？

Sub SimpleTextFile()
    Dim fileName As String
    fileName = ThisWorkbook.Path & "\TestTextFile.csv"

    Open fileName For Output As #1
        Print #1, "Print line 1"
        Write #1, "Print line 2"
        Print #1, 1
        Print #1, 123
        Write #1, 2
    Close #1
End Sub