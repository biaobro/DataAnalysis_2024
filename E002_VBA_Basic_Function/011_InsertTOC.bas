' 需求分析
' 用户点击按钮
' 弹窗提示
' 据弹窗做进一步动作
'   用户选择Cell —— 得到Cell —— 在Cell中插入内容
'   用户取消 —— 取消

Sub Auto_Table_Contents()
  Dim startCell As Range
  Dim msgConfirm As VBA.VbMsgBoxResult

  msgConfirm = VBA.MsgBox("The values in cells could be overwritten. Would you like to continue?", _
  VBA.vbOKCancel + VBA.vbDefaultButton2)
  If msgConfirm = VBA.vbCancel Then Exit Sub

    'On Error GoTo Leave  ' If user select nothing and press cancel, the code should be exit immediately
    On Error Resume Next

    Set startCell = Excel.Application.InputBox("Where?" _
    & VBA.vbNewLine & "Please select a cell :", "Insert Table of Contents", , , , , , 8)

    If VBA.Err.Number = 424 Then Exit Sub

      On Error GoTo Handle

      Set startCell = startCell.Cells(1, 1)
      Debug.Print startCell.Address


      Dim sht As Worksheet
      For Each sht In ThisWorkbook.Worksheets
        Debug.Print sht.Name
        If ActiveSheet.Name <> sht.Name Then
          If sht.Visible = xlSheetVisible Then
            ' 'sht.Name' to escape space in the name
            ActiveSheet.Hyperlinks.Add Anchor:=startCell, Address:="", SubAddress:= _
            "'" & sht.Name & "'!A1", TextToDisplay:=sht.Name
            startCell.Offset(0, 1).Value = sht.Range("A1").Value
            Set startCell = startCell.Offset(1, 0)
          End If 'sheet is visible
        End If
      Next sht

      Handle:


End Sub
