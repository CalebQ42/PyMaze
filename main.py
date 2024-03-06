import time
from tkinter import Canvas, Tk

class TkWindow:
    def __init__(self, title="DO A MAZE", width = 800, height = 600):
        self.width = width
        self.height = height
        self.show = True
        self.win = Tk()
        self.win.title(title)
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.win.call('tk', 'scaling', 5.0)
        self.__canvas = Canvas(background="black")
        self.__canvas.pack()
        self.update_window()

    def open_and_wait(self):
        while self.show:
            self.update_window()
        self.win.destroy()

    def update_window(self):
        self.win.update_idletasks()
        self.win.update()

    def close(self):
        self.show = False

    def draw_line(self, line, color="white"):
        self.__canvas.create_line(line.x_1, line.y_1, line.x_2, line.y_2, fill=color, width=2)

class Line:
    def __init__(self, x_1, y_1, x_2, y_2):
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2

class Cell:
    def __init__(self, x, y, win, size=50):
        self.x = x
        self.y = y
        self.__win = win
        self.size = size
        self.top = True
        self.bottom = True
        self.right = True
        self.left = True
        self.visited = False

    def draw(self):
        #top
        self.__draw_line(
            Line(self.x, self.y, self.x+self.size, self.y),
            self.top
        )
        #bottom
        self.__draw_line(
            Line(self.x, self.y+self.size, self.x+self.size, self.y+self.size),
            self.bottom
        )
        #right
        self.__draw_line(
            Line(self.x+self.size, self.y, self.x+self.size, self.y+self.size),
            self.right
        )
        #left
        self.__draw_line(
            Line(self.x, self.y, self.x, self.y+self.size),
            self.left
        )

    def __draw_line(self, line, exists):
        if exists:
            self.__win.draw_line(line, "white")
        else:
            self.__win.draw_line(line, "black")

class Maze:
    def __init__(self, x, y, rows, cols, win, cell_size=50):
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.__create_cells()

    def __create_cells(self):
        self.cells = []
        prev = 0
        x, y = 0, 0
        while x < self.rows or y < self.cols:
            if x >= len(self.cells):
                self.cells.append([])
            self.cells[x].append(
                Cell(
                    self.x+(self.cell_size*x), self.y+(self.cell_size*y), self.win, self.cell_size
                )
            )
            print(x, y)
            print(len(self.cells), len(self.cells[x]))
            self.cells[x][y].draw()
            self.win.update_window()
            time.sleep(0.05)
            if prev <= self.cols:
                if y <= 0:
                    prev += 1
                    x = 0
                    y = prev
                    continue
            else:
                if x >= self.row:
                    prev += 1
                    x = prev - self.cols
                    y = self.rows - 1
                    continue
            x += 1
            y -= 1
        print("YO")

    def __is_init(self, x, y):
        if x >= len(self.cells):
            return False
        return y < len(self.cells[x])

def main():
    win = TkWindow()
    mz = Maze(25, 25, 10, 10, win)
    win.open_and_wait()

main()