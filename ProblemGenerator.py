class ProblemGenerator:

    def generate_sudoku(self):
        """
        Létrehoz egy Sudoku feladványt: először egy teljesen kitöltött táblát,
        majd véletlenszerűen eltávolít számokat, hogy kirakható legyen.
        """
        self.clear_grid()  # Tábla törlése

        # 1. Létrehoz egy teljesen kitöltött Sudoku táblát
        sudoku_grid = self.create_complete_sudoku()

        # 2. Véletlenszerűen eltávolít néhány számot (nehézségi szint alapján)
        self.remove_numbers_from_grid(sudoku_grid, empty_cells=40)

        # 3. A generált feladványt megjeleníti a rácson
        for row in range(9):
            for col in range(9):
                if sudoku_grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(sudoku_grid[row][col]))

        messagebox.showinfo("Generate", "Sudoku problem generated!")


    def create_complete_sudoku(self):
        """
        Létrehoz egy helyesen kitöltött Sudoku táblát backtracking algoritmus segítségével.
        """
        def is_valid(board, row, col, num):
            # Ellenőrzi, hogy az adott szám elhelyezhető-e a pozícióban
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
        """
        Eltávolít véletlenszerű számokat a teljes Sudoku tábláról.
        """
        count = empty_cells
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if grid[row][col] != 0:
                grid[row][col] = 0
                count -= 1