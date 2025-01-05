

Option Explicit

Sub Find_One()
    Dim compID As Range
    Range("C3").ClearContents
    Set compID = Range("A:A").Find(what:=Range("B3").Value, _
                                    LookIn:=xlValues, _
                                    LookAt:=xlWhole)
    '要写成 Not object Is Nothing
    'object Is Not Nothing 报错
    If Not compID Is Nothing Then
        Range("C3").Value = compID.Offset(0, 4).Value
    Else
        MsgBox "Company not found"
    End If
End Sub


Sub Find_Many()
    Dim compID As Range
    Dim firstMatch As Variant

    Range("D3").ClearContents

    Set compID = Range("A:A").Find(what:=Range("B3").Value, _
                                    LookIn:=xlValues, _
                                    LookAt:=xlWhole)
    '要写成 Not object Is Nothing
    'object Is Not Nothing 报错
    If Not compID Is Nothing Then
        Range("D3").Value = compID.Offset(0, 4).Value
        firstMatch = compID.Address
        Do
            Set compID = Range("A:A").FindNext(compID)
            If compID.Address = firstMatch Then Exit Do
            Range("D3").Value = Range("D3").Value & ", " & compID.Offset(0, 4).Value

        Loop
    Else
        MsgBox "Company not found"
    End If
End Sub