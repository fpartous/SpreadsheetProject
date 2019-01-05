from Spreadsheet import Sheet
from user_interface import Test

'''
s = Sheet(5, 5)


s.updateValue2("A1", "7")

s.updateValue2("B2", "5")
s.updateValue2("B4", "5")
s.updateValue2("C2", "5")

s.updateValue2("A2", "=21+A3") #TODO: ranges in the coordinates of updateValue2()
print(s)

s.searchAndReplace(5, 6)
print(s)

s.undo()
print(s)
s.undo()
print(s)
s.undo()
print(s)
s.undo()
print(s)
s.redo()
print(s)
s.redo()
print(s)
s.undo()
print(s)
s.redo()
print(s)
s.updateValue2("A1", "8")
print(s)
s.undo()
print(s)
'''





if __name__ == "__main__":
        app = Test(8, 4)
        app.mainloop()








