import sys
import time
import random

from tkinter import Canvas, Tk

class TkWindow:
    def __init__(self, title="DO A MAZE", width = 800, height = 600):
        self.width = width
        self.height = height
        self.show = True
        self.win = Tk()
        self.win.geometry(f"={width}x{height}")
        self.win.title(title)
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.win.call('tk', 'scaling', 5.0)
        self.__canvas = Canvas(background="black", height=height, width=width)
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
    def __init__(self, x, y, win=None, size=50):
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
        if not self.__win:
            return
        if exists:
            self.__win.draw_line(line, "white")
        else:
            self.__win.draw_line(line, "black")

class Maze:
    def __init__(self, x, y, rows, cols, win=None, cell_size=50, seed=None):
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
        while start_x < self.cols and start_y < self.rows:
            if x >= len(self.cells):
                self.cells.append([])
            self.cells[x].append(
                Cell(
                    self.x+(self.cell_size*x), self.y+(self.cell_size*y), self.win, self.cell_size
                )
            )
            if self.win:
                self.cells[x][y].draw()
                self.win.update()
                time.sleep(0.01)
            x += 1
            y -= 1
            if y < 0 or x >= self.cols:
                if start_y >= self.rows-1:
                    start_x += 1
                else:
                    start_y += 1
                x = start_x
                y = start_y

    def __create_maze(self):
        self.cells[0][0].top = False
        self.cells[self.cols-1][self.rows-1].bottom = False
        self.cells[0][0].draw()
        self.cells[self.cols-1][self.rows-1].draw()
        if self.seed:
            random.seed = self.seed
        self.__create_path(0, 0)
    
    def __create_path(self, x, y):
        cell = self.cells[x][y]
        cell.visited = True
        possible = []
        if y > 0 and not self.cells[x][y-1].visited: # up
            possible.append(0)
        if x < self.cols-1 and not self.cells[x+1][y].visited: # right
            possible.append(1)
        if y < self.rows-1 and not self.cells[x][y+1].visited: # down
            possible.append(2)
        if x > 0 and not self.cells[x-1][y].visited: # left
            possible.append(3)
        if not possible:
            return
        while possible:
            rand = random.randint(0, len(possible)-1)
            move = possible[rand]
            possible.remove(move)
            if move == 0:
                move_to = self.cells[x][y-1]
                if move_to.visited:
                    continue
                cell.top = False
                move_to.bottom = False
                if self.win:
                    cell.draw()
                    move_to.draw()
                    self.win.update()
                    time.sleep(0.01)
                self.__create_path(x, y-1)
            elif move == 1:
                move_to = self.cells[x+1][y]
                if move_to.visited:
                    continue
                cell.right = False
                move_to.left = False
                if self.win:
                    cell.draw()
                    move_to.draw()
                    self.win.update()
                    time.sleep(0.01)
                self.__create_path(x+1, y)
            elif move == 2:
                move_to = self.cells[x][y+1]
                if move_to.visited:
                    continue
                cell.bottom = False
                move_to.top = False
                if self.win:
                    cell.draw()
                    move_to.draw()
                    self.win.update()
                    time.sleep(0.01)
                self.__create_path(x, y+1)
            else:
                move_to = self.cells[x-1][y]
                if move_to.visited:
                    continue
                cell.left = False
                move_to.right = False
                if self.win:
                    cell.draw()
                    move_to.draw()
                    self.win.update()
                    time.sleep(0.01)
                self.__create_path(x-1, y)

    def __reset_visited(self):
        for row in self.cells:
            for c in row:
                c.visited = False

    def solve(self):
        self.__reset_visited()
        return self.__solve_actual(0, 0)

    def __solve_actual(self, x, y):
        if x == self.cols-1 and y == self.rows-1:
            return True
        cur = self.cells[x][y]
        cur.visited = True
        dirs = []
        if not cur.bottom: #down
            dirs.append((x, y+1))
        if not cur.right: #right
            dirs.append((x+1, y))
        if not cur.left: #left
            dirs.append((x-1, y))
        if not cur.top and not (x == 0 and y == 0): #up
            dirs.append((x, y-1))
        for d in dirs:
            to = self.cells[d[0]][d[1]]
            if to.visited:
                continue
            if self.win:
                self.__paint_solve_path(cur, to)
                self.win.update()
                time.sleep(0.05)
            res = self.__solve_actual(d[0], d[1])
            if res:
                return True
            if self.win:
                self.__paint_solve_path(cur, to)
                self.win.update()
                time.sleep(0.05)
        return False
        

    def __paint_solve_path(self, cur, to):
        if not self.win:
            return
        color = "red"
        if to.visited:
            color = "gray"
        self.win.draw_line(
            Line(
                cur.x + cur.size//2, cur.y + cur.size//2, to.x + cur.size//2, to.y + cur.size//2
            ), color=color
        )

def main():
    win = TkWindow(width=1550, height=1550)
    sys.setrecursionlimit(5000)
    mz = Maze(25, 25, 50, 50, win, cell_size=30)
    mz.solve()
    win.open_and_wait()

if __name__ == "__main__":
    main()
