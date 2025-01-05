' One-Dimension —— LBOUND,UBOUND
'   LBOUND 默认是0，除非显示指定
' Dynamic Array
'   Redim
'   Redim Preserve —— 保留已填充的值


Option Explicit

Sub Array_Preserve()
    Dim Cust() As String
    ReDim Cust(1 To 2)

    Cust(1) = "wu"
    Cust(2) = "chen"

    ' Pay attention to the different Redim
    'ReDim Cust(1 To 3)
    ReDim Preserve Cust(1 To 3)
    Cust(3) = "wei"

    MsgBox Cust(1) & vbNewLine & Cust(2) & vbNewLine & Cust(3)

End Sub