from user_interface import RunInterface

class Run(object):
    def __init__(self, rows, cols, data):
        RunInterface.starting_1(rows, cols, data)

    # def create_newSheet(self, rows, cols, data):
    #     new_sheet = Sheet(rows, cols)
    #     for i in range(rows):
    #         for j in range(cols):
    #             new_sheet.updateValue(i, j, data[i][j])
    #     app = RunInterface(rows, cols)
    #     app.mainloop()


if __name__ == "__main__":
    app = RunInterface(100, 100)
    app.mainloop()