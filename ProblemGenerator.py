import random
from tkinter import messagebox


class ProblemGenerator:
    def generate_sudoku(self, entries, callback):

        grid = self.create_complete_sudoku()
        self.remove_numbers_from_grid(grid, empty_cells=40)
        
        for row in range(9):
            for col in range(9):
                if grid[row][col] != 0:
                    entries[row][col].insert(0, str(grid[row][col]))
        messagebox.showinfo("Generate", "Sudoku problem generated!")
    
    def create_complete_sudoku(self):
        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
                if board[row // 3 * 3 + i // 3][col // 3 * 3 + i % 3] == num:
                    return False
            return True
        
        def fill_grid(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        random.shuffle(numbers)
                        for num in numbers:
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if fill_grid(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True
        
        board = [[0 for _ in range(9)] for _ in range(9)]
        numbers = list(range(1, 10))
        fill_grid(board)
        return board

    def remove_numbers_from_grid(self, grid, empty_cells):
        count = empty_cells
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if grid[row][col] != 0:
                grid[row][col] = 0
                count -= 1
    
    
