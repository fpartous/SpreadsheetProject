import re
from Matrix import Matrix
from math import *


class NumberCell(object):
    def __init__(self, x, coordinates):
        self.value = int(x)
        self.coordinates = coordinates

    def __str__(self):
        return str(self.value)

    def updateValue(self):
        print self.coordinates, " got updated"
        return True


class FormulaCell(object):
    def __init__(self, expr, sheet, coordinates):  # expr is of the shape "=A1+B2" in string
        self._sheet = sheet
        self.formula = expr
        self.ListOfDependencies = []    # List of cells upon which the current cell depends
        self.createDependencyList()
        self.coordinates = coordinates
        self.updateValue()

    def updateValue(self):
        for coord in self.ListOfDependencies: # make sure all cells this one depends on update their values first
            cellObj = self._sheet.getCellObject(coord[0], coord[1])
            cellObj.updateValue() # TODO: implement visited list and check for self referential loops
        if(self.formula[0] == "="):
            self.value = eval(self.addCalls(self.formula[1:]))
        else:
            self.value = eval(self.addCalls(self.formula[0:]))
        print self.coordinates, " got updated"

    def createDependencyList(self):  # look for all dependencies in the formula
        input = self.formula[0:]
        self.ListOfDependencies = [] # first empty the list, will then be refilled
        p = re.compile('[A-Z]+[1-9][0-9]*')
        matches = p.finditer(input)
        for match in matches:
            coordinate_string = input[match.start():match.end()]
            coordinates = self._sheet.coordstringToRowCol(coordinate_string)
            if coordinates not in self.ListOfDependencies: #look if these coordinates are already is the list of dependencies. If not, add them
                self.ListOfDependencies.append(coordinates)

    def expandRanges(self, input):  # expand the ranges(eg: A1:A5 --> A1, A2, A3, A4, A5)
        p_ranges = re.compile('[A-Z]+[1-9][0-9]*[:][A-Z]+[1-9][0-9]*')
        p_letters = re.compile('[A-Z]+')
        p_numbers = re.compile('[1-9][0-9]*')
        matches = p_ranges.finditer(input)
        result = []
        prev = 0
        for match in matches:
            result.append(input[prev:match.start()])
            match_string = input[match.start():match.end()]

            matches_letters = p_letters.finditer(match_string)
            matches_numbers = p_numbers.finditer(match_string)
            letters = [match_string[match_letters.start():match_letters.end()] for match_letters in matches_letters]
            letters_int = [self._sheet.colNameToInt(l) for l in letters]
            numbers = [int(match_string[match_numbers.start():match_numbers.end()]) for match_numbers in
                       matches_numbers]
            result.append('[')
            for i in range(letters_int[0], letters_int[1] + 1):
                for j in range(numbers[0], numbers[1] + 1):
                    result.append(self._sheet.intToColName(i) + str(j))
                    if not (i == letters_int[1] and j == numbers[1]):
                        result.append(', ')
                    else:
                        result.append(']')
            prev = match.end()

        result.append(input[prev:])
        resultString = ''.join(result)
        return resultString

    # transforms the formula stored in a cell into python code
    # so A1 => self.lookup('A1')
    # A1 + B1 => self.lookup('A1') + self.lookup('B1')
    def addCalls(self, input):
        input = self.expandRanges(input)

        p = re.compile('[A-Z]+[1-9][0-9]*')
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

    def coordstringToRowCol(self, coordinate_string): #input is for example AB12, output is then [12, 27]
        p_letters = re.compile('[A-Z]+')
        p_numbers = re.compile('[1-9][0-9]*')

        matches_letters = p_letters.finditer(coordinate_string)
        matches_numbers = p_numbers.finditer(coordinate_string)
        letters = [coordinate_string[match_letters.start():match_letters.end()] for match_letters in matches_letters]
        letters_int = [self.colNameToInt(l) for l in letters]
        numbers = [int(coordinate_string[match_numbers.start():match_numbers.end()]) for match_numbers in matches_numbers]
        return [numbers[0] - 1, letters_int[0]]

    def updateValue2(self, coordinate_string, newValue): #coordinate_string should be something like A5
        result = self.coordstringToRowCol(coordinate_string)
        self.updateValue(result[0], result[1], newValue)

    def updateValue(self, row, col, newValue):
        if newValue.isdigit():
            cellObject = NumberCell(newValue, [row, col])
        else:
            cellObject = FormulaCell(newValue, self, [row, col])
        self.matrix.setElementAt(row, col, cellObject)

        # self.checkAllDependenciesForUpdates()

        # lookup the value of a given cell.
        # x = A1, B22, AB33 ...

    def getCellObject(self, row, col): #get the NumberCell or Formulacell object at the given coordinates
        return self.matrix.getElementAt(row, col)

    def colNameToInt(self, name):
        result = 0
        for i in range(len(name)):
            result += (ord(name[i]) - 65 + 1) * 26 ** (len(name) - 1 - i)

        return result - 1

    def intToColName(self, x):
        uppercases = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 0 = A, 25 = Z
        result = []
        if x >= 0:
            rest = x % 26
            x = (x // 26)
            result.insert(0, uppercases[rest])  # prepend the uppercase letter to the resulting list
        while x > 0:
            rest = x % 26
            x = (x // 26)
            result.insert(0, uppercases[rest - 1])  # prepend the uppercase letter to the resulting list
        resultString = ''.join(result)
        return resultString

    def lookup(self, x):
        p = re.compile('[A-Z]+')
        matches = p.match(x)
        to = matches.end()
        letters = x[:to]
        digits = x[to:]
        row = int(digits) - 1  # for 0 based matrix index
        col = self.colNameToInt(letters)
        cell = self.matrix.getElementAt(row, col)
        return cell.value

    def __str__(self):
        return self.matrix.__str__()

