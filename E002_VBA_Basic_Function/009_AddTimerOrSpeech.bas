

Sub Find_Many()
    Dim compID As Range
    Dim firstMatch As Variant
    Dim counter As Byte
    counter = 0

    Dim start
    start = VBA.Timer


    Range("D3").ClearContents


    Set compID = Range("A:A").Find(what:=Range("B3").Value, _
                                    LookIn:=xlValues, _
                                    LookAt:=xlWhole)
    '要写成 Not object Is Nothing
    'object Is Not Nothing 报错
    If Not compID Is Nothing Then
        Range("D3").Value = compID.Offset(0, 4).Value
        counter = 1
        firstMatch = compID.Address
        Do
            Set compID = Range("A:A").FindNext(compID)
            If compID.Address = firstMatch Then Exit Do
            counter = counter + 1
            Range("D3").Value = Range("D3").Value & ", " & compID.Offset(0, 4).Value

        Loop
    Else
        MsgBox "Company not found"
    End If
    Application.Speech.Speak "干得漂亮 " & counter & " matches has been found." & " 用时 " & (Timer - start) & "秒"
End Sub
