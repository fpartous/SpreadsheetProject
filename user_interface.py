try:
    import Tkinter as tk
    from ttk import *
    import tkFont
except:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.font as tkFont


class Table(tk.Frame):
    def __init__(self, parent, sheet, height, title=""):
        tk.Frame.__init__(self, parent)
        self._title = tk.Label(self, text=title, background="#ECCCCE", font=("Helvetica", 16))
        try:
            self._tree = Treeview(self, height=height, show="headings")
        except:
            self._tree = ttk.Treeview(self, height=height, show="headings")
        self._widgets = []
        self.sheet = sheet
        self.showTable()

    def showTable(self):
        current_row = []
        headers_some = [self.sheet.intToColName(i) for i in range(self.sheet.getCols())]
        i = 0
        for header in headers_some:
            label = tk.Label(self, text="%s" % header, borderwidth=3, width=10)
            label.grid(row=2, column=i+1, padx=1, pady=1)
            i += 1
            current_row.append(label)
        self._widgets.append(current_row)

        j=1
        for row in range(1, self.sheet.getRows()+1):
            current_row = []
            self._tree.insert('', 'end', values=row+1)
            label = tk.Label(self, text="%s" % j, borderwidth=0, width=10)
            label.grid(row=row + 2, column=0, padx=1, pady=1)
            current_row.append(label)
            j += 1
            for column in range(self.sheet.getCols()):
                label = tk.Label(self, text="%s" % self.sheet.getValue(row-1, column), borderwidth=0, width=10)
                label.grid(row=row+3-1, column=column+1, padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


class RunInterface(tk.Tk):
    def __init__(self, parent, sheet):
        tk.Tk.__init__(self)
        self.sheet = sheet
        self.parent = parent
        self.font = tkFont.Font(weight='bold')
        self.cell_label = tk.Label(self, text="Cell:", font=self.font)
        self.cell_input = tk.Entry(self, textvariable="", width=30)
        self.formula_label = tk.Label(self, text="Formula:", font=self.font)
        self.formula_input = tk.Entry(self, textvariable="", width=30)
        self.button_run = tk.Button(self, text="Run", command=self.run_sheet, height=2, width=8)
        self.file_label = tk.Label(self, text="File:", font=self.font)
        self.file_input = tk.Entry(self, textvariable="", width=60)
        self.button_import = tk.Button(self, text="Import", command=self.import_file, height=2, width=8)
        self.button_export = tk.Button(self, text="Export", command=self.export_file, height=2, width=8)
        # self.starting()
        self.sheet_table = Table(self, self.sheet, height=self.sheet.getRows(), title="Sheet")
        self.show_grid()

    def show_grid(self):
        self.cell_label.grid(row=0, column=1, sticky=tk.W)
        self.formula_label.grid(row=0, column=2, sticky=tk.W)
        self.cell_input.grid(row=1, column=1, sticky=tk.W)
        self.formula_input.grid(row=1, column=2, sticky=tk.W)
        self.button_run.grid(row=0, column=3, rowspan=2, sticky=tk.S)
        self.file_label.grid(row=2, column=1, sticky=tk.W)
        self.file_input.grid(row=3, column=1, sticky=tk.W, columnspan=2)
        self.button_import.grid(row=2, column=3, rowspan=2, sticky=tk.S)
        self.button_export.grid(row=2, column=4, rowspan=2, sticky=tk.S)
        self.sheet_table.grid(row=4, column=1, columnspan=4)

    def starting(self):
        # x = Sheet(30, 4)
        self.sheet.updateValue(0, 0, '7')  # A1
        self.sheet.updateValue(0, 1, '5')  # B1
        # x.updateValue(1, 0, '(3+4)*2')  #A2
        self.sheet.updateValue(2, 0, '=A1+B1')  # A3
        # x.updateValue2(2, 1, '=A1-B1')   #C2
        # x.updateValue2(2, 2, '=A1*B1')   #C3
        # x.updateValue(26, 0, '9')       #AA1
        # x.updateValue2(3, 0, '=AA1')     #D1
        # x.updateValue2(4, 1, '=sum([A1+B1+C1])') #E2
        self.sheet.updateValue(4, 3, '=sum(A1:B3)')  # D5
        # x.updateValue(4, 2, '=average(A1:A3)')  # C5
        # x.updateValueCoord('B2', '6')
        # x.updateValueCoord('B4', '23')
        # x.updateValueCoord('D4', '=sum(A1:B3)')
        self.sheet.updateValue2('A1', '2')

    def starting_1(self, rows, cols, data):
        for i in range(rows):
            for j in range(cols):
                self.sheet.updateValue(i, j, data[i][j])

    def run_sheet(self):
        cell = self.cell_input.get()
        cell_split = cell.split(',')
        formula = self.formula_input.get()
        if len(cell_split) > 1:
            pos_x = int(cell_split[0])
            pos_y = int(cell_split[1])
            self.sheet.updateValue(pos_x, pos_y, formula)
            # self.sheet_table.set(pos_x, pos_y, self.sheet.getValue(pos_x, pos_y))
            self.sheet_table.showTable()
        else:
            self.sheet.updateValue2(cell, formula)
            self.sheet_table.showTable()

    def import_file(self):
        self.parent.reading_file(self.file_input.get())

    def export_file(self):
        self.parent.writing_csv_file(self.file_input.get())

# if __name__ == "__main__":
#     app = RunInterface()
#     app.mainloop()
