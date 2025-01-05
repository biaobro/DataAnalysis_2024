' Check If file or Folder Exist
'   Dir[(path,[attributes])]
'   attributes
'     vbNormal 默认
'     vbReadOnly 只读文件
'     vbHidden 隐藏文件
'     vbSystem 系统文件
'     vbDirectory 目录
'   完整的写法 —— vba.FileSystem.Dir()
' Wildcards (* ?)


Sub file_exist()
    Dim fileName As String
    fileName = VBA.FileSystem.Dir("C:\Users\weibiao.wb\Downloads\S10_Looping_Start.xlsm")

    If fileName = VBA.Constants.vbNullString Then
        MsgBox "file doesn't exists"
    Else
        MsgBox fileName
        Workbooks.Open "C:\Users\weibiao.wb\Downloads\" & fileName
    End If
End Sub


Sub folder_exist()
    Dim path As String
    Dim folder As String

    Dim answer As VbMsgBoxResult

    path = "C:\Users\weibiao.wb\Downloads\2021"
    folder = VBA.FileSystem.Dir(path, VBA.vbDirectory)

    If folder = VBA.Constants.vbNullString Then
        answer = MsgBox("Path doesn't exist. Would you like to create it?", vbYesNo, "Create Path")
        Select Case answer
            Case vbYes
                VBA.FileSystem.MkDir (path)
            Case Else
                Exit Sub
        End Select
    End If
End Sub