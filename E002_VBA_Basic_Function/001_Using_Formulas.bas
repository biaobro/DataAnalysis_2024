
'FormulaR1C1：使用行号和列号来引用单元格
'Formula：使用A1类型来引用单元格
'FormulaLocal：以本地语言显示公式

Sub excelFormula()
    Dim r As Long
    Dim lastRow As Long
    lastRow = Range("A" & Rows.Count).End(xlUp).Row

    Range("F9").FormulaR1C1 = "=IF(VALUE(LEFT(RC[-4],1))=8,RC[-1]-50,"""")"
    Range("F9").AutoFill Destination:=Range("F9:F85")
    Application.Calculate

    'reset color
    Range("A9", "E" & lastRow).Interior.Color = Excel.Constants.xlNone

    'alter color if value in F < 100
    For r = 9 To lastRow
        If Range("F" & r).Value < 100 Then
            Range("A" & r, "E" & r).Interior.Color = VBA.ColorConstants.vbRed
        End If
    Next r
End Sub