from Spreadsheet import Sheet

s = Sheet(30, 30)
s.updateValue(0, 0, "7")
s.updateValue(0, 1, "5")

s.updateValue(1, 0, "(3+4)*2")
s.updateValue(2, 0, "=A1+B1")
s.updateValue(2, 1, "=A1-B1")
s.updateValue(2, 2, "=A1*B1")
s.updateValue(3, 0, "=(A1+8)/A2")
s.updateValue(1, 0, "=AA1")
s.updateValue(0, 1, "55")
s.updateValue(0, 3, "66")
s.updateValue(0, 0, "sum([A2, A3, A4, A5])")
s.updateValue(0, 0, "average([A2, A3, A4, A5])")


print(s)




