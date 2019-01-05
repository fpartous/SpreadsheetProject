from user_interface import RunInterface

'''
s = Sheet(30, 30)
s.updateValue2("A1", "7")
s.updateValue2("B2", "5")
s.updateValue2("A2", "=21+A3") #TODO: ranges in the coordinates of updateValue2()
s.updateValue2("A3", "23")
s.updateValue2("A4", "1")
s.updateValue2("A5", "=A1+A2")

s.updateValue(1, 0, "(3+4)*2")
s.updateValue(2, 0, "=A1+B1")
s.updateValue(2, 1, "=A1-B1")
s.updateValue(2, 2, "=A1*B1")
s.updateValue(3, 0, "=(A1+8)/(A2+1)")
s.updateValue(1, 0, "=AA1")
s.updateValue(0, 1, "55")
s.updateValue(0, 3, "66")
s.updateValue(0, 0, "sum([A2, A3, A4, A5])")
s.updateValue(0, 0, "average([A2, A3, A4, A5])")
'''
# print(s)
if __name__ == "__main__":
    app = RunInterface(30, 4)
    app.mainloop()







