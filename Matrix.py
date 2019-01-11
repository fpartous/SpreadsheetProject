class Matrix(object):
    """A simple Matrix class in Python"""

    def __init__(self, rows, columns):
        self.width = columns
        self.height = rows
        self.data = []
        for i in range(rows):
            self.data.append([])
            for j in range(columns):
                self.data[i].append(0)

    def setElementAt(self, x, y, value):
        self.data[x][y] = value

    def getElementAt(self, x, y):
        return self.data[x][y]

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

    def addCol(self):
        for row in range(self.height):
            for col in range(self.width+1, self.width+2):
                self.data[row].append(0)
        self.width += 1

    def addRow(self):
        for row in range(self.height, self.height+1):
            self.data.append([])
            for col in range(self.width):
                self.data[row].append(0)

        self.height +=1

    def __str__(self):
        result = []
        result.append('\t')
        for i in range(self.width):
            result.append(self.intToColName(i) + '\t')
        result.append('\n')
        for rowNr in range(len(self.data)):
            result.append(str(rowNr + 1))
            result.append('\t')
            for cell in self.data[rowNr]:
                result.append(str(cell))
                result.append("\t")
            result.append("\n")
        string = ''.join(result)
        return string


