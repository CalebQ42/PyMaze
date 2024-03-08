import time
import random

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
        self.update()

    def open_and_wait(self):
        while self.show:
            self.update()
        self.win.destroy()

    def update(self):
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

    def can_remove_walls(self):
        num_walls = 0
        if self.top:
            num_walls += 1
        if self.right:
            num_walls += 1
        if self.bottom:
            num_walls += 1
        if self.left:
            num_walls += 1
        return num_walls > 2

    def __draw_line(self, line, exists):
        if exists:
            self.__win.draw_line(line, "white")
        else:
            self.__win.draw_line(line, "black")

class Maze:
    def __init__(self, x, y, rows, cols, win, cell_size=50, seed=None):
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.win = win
        self.seed = seed
        self.__create_cells()
        self.__create_maze()

    def __create_cells(self):
        self.cells = []
        start_x, start_y = 0, 0
        x, y = 0, 0
        while start_x < self.rows and start_y < self.cols:
            if x >= len(self.cells):
                self.cells.append([])
            self.cells[x].append(
                Cell(
                    self.x+(self.cell_size*x), self.y+(self.cell_size*y), self.win, self.cell_size
                )
            )
            self.cells[x][y].draw()
            self.win.update()
            time.sleep(0.05)
            x += 1
            y -= 1
            if y < 0 or x >= self.rows:
                if start_y >= self.cols-1:
                    start_x += 1
                else:
                    start_y += 1
                x = start_x
                y = start_y

    def __create_maze(self):
        self.cells[0][0].top = False
        self.cells[self.rows-1][self.cols-1].bottom = False
        self.cells[0][0].draw()
        self.cells[self.rows-1][self.cols-1].draw()
        if self.seed:
            random.seed = self.seed

def main():
    win = TkWindow()
    mz = Maze(25, 25, 10, 10, win)
    win.open_and_wait()

main()