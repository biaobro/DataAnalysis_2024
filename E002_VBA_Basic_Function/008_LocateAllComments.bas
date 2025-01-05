

Option Explicit

Sub Document_All_Comment()
    Dim newSht As Worksheet
    Dim sht As Worksheet
    Dim commentCounter As Long
    Dim cmt As Comment

    Set newSht = ThisWorkbook.Worksheets.Add
    Range("A1:C1") = Array("Comment", "Address", "Author")
    'On Error Resume Next

    For Each sht In ThisWorkbook.Worksheets
        commentCounter = 0
        Debug.Print sht.Name

        For Each cmt In sht.Comments
            Range("A" & (newSht.UsedRange.Rows.Count + 1)).Value = cmt.Text
            Range("B" & (newSht.UsedRange.Rows.Count)).Value = cmt.Parent.Address
            Range("C" & (newSht.UsedRange.Rows.Count)).Value = cmt.Author


            ' 定义名称
            ActiveWorkbook.Names.Add Name:=sht.Name & "_" & commentCounter, RefersTo:="=" & sht.Name & "!" & cmt.Parent.Address

      '添加超链接，链接到名称。不支持直接链接到单元格
            ActiveSheet.Hyperlinks.Add Anchor:=Range("B" & (newSht.UsedRange.Rows.Count)), Address:="", SubAddress:=sht.Name & "_" & commentCounter, TextToDisplay:=cmt.Parent.Address '"$D$7"

            commentCounter = commentCounter + 1

        Next cmt

    Next sht
End Sub
