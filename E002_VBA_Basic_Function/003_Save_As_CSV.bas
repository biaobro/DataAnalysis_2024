'Default Delimiter


Option Explicit

Sub saveAs()
    Dim filName As String
    Dim newBook As Workbook

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    filName = ThisWorkbook.Path & "\TestTextCSV.csv"

    Set newBook = Workbooks.Add
    Sheet1.Copy Before:=newBook.Sheets(1)

    With newBook
        .Sheets(1).Rows("1:3").Delete
        .saveAs Filename:=filName, FileFormat:=xlCSV
        .Close
    End With

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

End Sub