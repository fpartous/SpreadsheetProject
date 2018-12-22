import re
from Matrix import Matrix
from math import *


class NumberCell():
    def __init__(self, x):
        self.value = int(x)

    def __str__(self):
        return str(self.value)


class FormulaCell():
    def __init__(self, expr, sheet):  # expr is of the shape "=A1+B2" in string
        self._sheet = sheet
        self.formula = expr
        self.updateValue()

    def updateValue(self):
        if(self.formula[0] == "="):
            self.value = eval(self.addCalls(self.formula[1:]))
        else:
            self.value = eval(self.addCalls(self.formula[0:]))



    def expandRange(self, input): #expand the ranges (eg: A1:A5 --> A1, A2, A3, A4, A5)
        p = re.compile('[A-Z]+[1-9]+[:][A-Z]+[1-9]+')
        matches = p.finditer(input)
        result = []
        prev = 0
        for match in matches:
            result.append(input[prev:match.start()])
            result.append('self._sheet.lookup(\'')
            result.append(input[match.start():match.end()])
            result.append('\')')
            prev = match.end()

        result.append(input[prev:])
        resultString = ''.join(result)
        return resultString

    # transforms the formula stored in a cell into python code
    # so A1 => self.lookup('A1')
    # A1 + B1 => self.lookup('A1') + self.lookup('B1')
    def addCalls(self, input):
        #input = self.expandRange(input) #expand the ranges (eg: A1:A5 --> A1, A2, A3, A4, A5)

        p = re.compile('[A-Z]+[1-90-9]+')
        matches = p.finditer(input) #if matches is empty then it's just a purely numerical expression --> put it in a number cell

        result = []
        prev = 0
        for match in matches:
            result.append(input[prev:match.start()])
            result.append('self._sheet.lookup(\'')
            result.append(input[match.start():match.end()])
            result.append('\')')
            prev = match.end()

        result.append(input[prev:])
        resultString = ''.join(result)
        return resultString

    def __str__(self):
        self.updateValue()
        return str(self.value)
def average(list):
    sum = 0.
    for el in list:
        sum += el
    return sum/len(list)

class Sheet(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = Matrix(rows, cols)
        # fill the sheet with zero numbercells
        for row in range(self.rows):
            for col in range(self.cols):
                self.updateValue(row, col, "0")

    def updateValue(self, row, col, newValue):
        if newValue.isdigit():
            cellObject = NumberCell(newValue)
        else:
            cellObject = FormulaCell(newValue, self)

        self.matrix.setElementAt(row, col, cellObject)
        # self.checkAllDependenciesForUpdates()

        # lookup the value of a given cell.
        # x = A1, B22, AB33 ...

    # A => 0

    def rowNameToInt(self, name):
        result = 0
        for i in range(len(name)):
            result += (ord(name[i]) - 65 + 1) * 26 ** (len(name) - 1 - i)

        return result - 1
    '''
    def intToRowName(self, x):
        result = ''
        i = x
        while i > 0:
    '''


    def lookup(self, x):
        p = re.compile('[A-Z]+')
        matches = p.match(x)
        to = matches.end()
        letters = x[:to]
        digits = x[to:]
        col = int(digits) - 1  # for 0 based matrix index
        row = self.rowNameToInt(letters)
        cell = self.matrix.getElementAt(row, col)
        return cell.value

    def __str__(self):
        return self.matrix.__str__()

