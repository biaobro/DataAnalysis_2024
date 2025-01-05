' 'Option
'   FilePicker
'   FolderPicker
'   DialogOpen
'   DialogSaveAs

Option Explicit

Sub loopInsideFolder()

    Dim folderName As String
    Dim fileName As String


    With Application.FileDialog(msoFileDialogFolderPicker)
        .Title = "Please select folder"
        .ButtonName = "Folder Picker"
        If .Show = 0 Then
            MsgBox "nothing was selected"
            Exit Sub
        Else
            folderName = .SelectedItems(1) & "\"
        End If
    End With

    fileName = VBA.FileSystem.Dir(folderName)

    ' "" equals to VBA.Constants.vbNullString
    Do Until fileName = ""
        Debug.Print fileName

        ' The argument should be whole path
        Workbooks.Open (folderName + fileName)

        ' no need arguments in the subsequent call!!!
        fileName = VBA.FileSystem.Dir
    Loop

End Sub

' Please notile the usage of DoEvents
Sub longLoop()
    Dim L As Long
    For L = 1 To 3000
    DoEvents 'allow windows to catchup
        Debug.Print L
    Next L
End Sub
