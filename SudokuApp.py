import random
import tkinter as tk
from tkinter import messagebox
from Board import Board  

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#333333")  # Ablak háttérszíne
        
        # Fő keret
        self.main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#333333")
        self.main_frame.pack()

        # Sudoku táblázat keret
        self.grid_frame = tk.Frame(self.main_frame, bg="#333333")
        self.grid_frame.pack()

        self.load_problem()
       # self.drawBoard() 
        self.draw_buttons()
        self.root.geometry("650x750")
        self.root.resizable(False, False)

    def drawBoard(self):
        self.entries = []
        for row in range(9):
            row_entries = []
            for col in range(9):
                # Szegélyek meghatározása a 3x3 blokkokhoz
                top_border = 2 if row % 3 == 0 else 1
                left_border = 2 if col % 3 == 0 else 1
                bottom_border = 2 if row == 8 else 1
                right_border = 2 if col == 8 else 1

                # Cellák létrehozása
                entry = tk.Entry(
                    self.grid_frame,
                    justify='center',
                    font=("Arial", 25),  # Nagyobb betűméret
                    relief="solid",
                    width=2,  # Nagyobb négyzetek
                    bd=0,
                    highlightthickness=0
                )
                entry.grid(
                    row=row,
                    column=col,
                    sticky="nsew",
                    padx=(left_border, right_border),
                    pady=(top_border, bottom_border),
                )
                row_entries.append(entry)

                # A Board.problem tömb értékének beállítása az Entry widgetekben
                if Board.problem[row][col] != 0:
                    entry.insert(tk.END, str(Board.problem[row][col]))  # Ha van érték, azt beírjuk
                entry.config(state='readonly')  # Ne lehessen szerkeszteni
               
            self.entries.append(row_entries)
     
    def draw_buttons(self):
                 # Gombok keret
        self.button_frame = tk.Frame(self.main_frame, pady=10, bg="#333333")
        self.button_frame.pack(fill=tk.X)
        
        # Gombok
        self.generate_button = tk.Button(
            self.button_frame, 
            text="Generate", 
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.generate_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.load_button = tk.Button(
            self.button_frame, 
            text="Load", 
            command=self.load_problem, 
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.load_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
        self.stop_button = tk.Button(
            self.button_frame, 
            text="Stop", 
            command=self.solve_sudoku, 
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.set_params_button = tk.Button(
            self.button_frame, 
            text="Set Parameters", 
            command=self.set_parameters, 
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.set_params_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.set_params_button = tk.Button(
            self.button_frame, 
            text="Clear", 
            command=self.clear_grid, 
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.set_params_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
          
    def load_problem(self):
        Board.set_problem(40)
        print(Board.problem)
        self.drawBoard()

    def solve_sudoku(self):
        # Sudoku megoldása
        messagebox.showinfo("Solve", "Solving Sudoku!")
        print(self.get_grid_values())
        
    def set_parameters(self):
        # Paraméterek beállítása
        messagebox.showinfo("Set Parameters", "Setting parameters!")
        pass

    def clear_grid(self):   
        for row_entries in self.entries:
            for entry in row_entries:
                entry.config(state='normal')
                entry.delete(0, tk.END)  # Töröljük a cellák tartalmát




    def get_grid_values(self):
        """
        Kiolvassa a sudoku tábla aktuális állapotát és eltárolja egy 9x9-es listában.
        Üres cellákat 0-val helyettesíti.
        """
        grid_values = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                row.append(int(value) if value.isdigit() else 0)  # Ha nem szám, akkor 0
            grid_values.append(row)
        return grid_values

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
