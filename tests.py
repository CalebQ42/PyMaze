import unittest

from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )
        for x in range(0, len(m1.cells)):
            for y in range(0, len(m1.cells[x])):
                self.assertFalse(
                    m1.cells[x][y].visited,
                    f"{x} {y} is visited, but shouldn't be"
                )
                
if __name__ == "__main__":
    unittest.main()
