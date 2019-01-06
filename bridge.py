from user_interface import RunInterface
from Spreadsheet import Sheet
import csv


class Run(object):
    def __init__(self, h, w):
        self.app = ''
        self.sheet = Sheet(h, w)
        self.create_run_interface(self.sheet)

    def writing_csv_file(self, path):
        file = open(path, 'w')
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in self.sheet.matrix.data:
            value = []
            for column in row:
                value.append(column)
            file_writer.writerow(value)
        file.close()

    def reading_file(self, path):
        file = open(path, 'r', encoding='utf-8-sig')
        list1 = list()
        i = 0
        j = 0
        for row in file:
            row = row.strip()
            column = row.split(';')
            list_temp = []
            i += 1
            j = len(column)
            for value in column:
                if value == '':
                    value = '0'
                list_temp.append(value)
            list1.append(list_temp)
        file.close()
        self.create_new_sheet(i, j, list1)

    def create_new_sheet(self, rows, cols, data):
        new_sheet = Sheet(rows, cols)
        for i in range(rows):
            for j in range(cols):
                new_sheet.updateValue(i, j, data[i][j])
        self.create_run_interface(new_sheet)

    def create_run_interface(self, sheet):
        self.app = RunInterface(self, sheet)
        self.app.mainloop()
