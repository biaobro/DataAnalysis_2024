
Option Explicit

Sub GetDataFromFile()
    Application.ScreenUpdating = False


    ' The type should be variant cause
    ' It return False while nothing selected
    ' even String works normal
    Dim fileToOpen As Variant

    fileToOpen = Application.GetOpenFilename(Title:="Choose File", FileFilter:="Excel Files(*.xlsx*),*.xlsx*")


    Dim targetBook As Workbook

    If fileToOpen = False Then

        Debug.Print "nothing selected"
    Else
        Set targetBook = Workbooks.Open(fileToOpen)
        targetBook.Sheets(1).UsedRange.Copy
        ThisWorkbook.Worksheets.Add.Range("A1").PasteSpecial xlPasteValues
        targetBook.Close
    End If

    Application.ScreenUpdating = True
    Application.CutCopyMode = False
End Sub