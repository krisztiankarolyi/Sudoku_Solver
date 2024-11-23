import asyncio
import threading
import tkinter as tk
from tkinter import messagebox
from Board import Board  
from GA import GA
from Population import Population
from Parameters import Parameters
from ProblemGenerator import ProblemGenerator

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#333333")  # Ablak háttérszíne
        self.problem_generator = ProblemGenerator()       
        # Fő keret
        self.main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#333333")
        self.main_frame.pack()

        # Sudoku táblázat keret
        self.grid_frame = tk.Frame(self.main_frame, bg="#333333")
        self.grid_frame.pack()

        self.load_problem()
            # self.drawBoard() 
        self.draw_buttons()
        self.draw_parameter_frame()
        self.root.geometry("600x750")
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
                    font=("Arial", 20),  # Nagyobb betűméret
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

        # Generate gomb
        self.generate_button = tk.Button(
            self.button_frame,
            text="Generate",
            command=lambda: self.problem_generator.generate_sudoku(self.entries, self.clear_grid()),
            bg="#555555",
            fg="white",
            font=("Arial", 12)
        )
        self.generate_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Load gomb
        self.load_button = tk.Button(
            self.button_frame, 
            text="Load", 
            command=self.load_problem, 
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.load_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Stop gomb
        self.stop_button = tk.Button(
            self.button_frame, 
            text="Stop", 
            command=self.stop_running,
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Solve gomb
        self.solve_button = tk.Button(
            self.button_frame, 
            text="Solve", 
            command=self.start_simulation,  # Wrapper metódus
            bg="#555555", 
            fg="white", 
            font=("Arial", 12)
        )
        self.solve_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.parameter_button = tk.Button(
            self.button_frame,
            text="Parameters",
            command=self.draw_parameter_frame,
            bg="#555555",
            fg="white",
            font=("Arial", 12),
        )
        self.parameter_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
           
    def load_problem(self):
        Board.set_problem(40)
        print(Board.problem)
        self.drawBoard()

    def set_parameters(self):
        # Paraméterek beállítása
        messagebox.showinfo("Set Parameters", "Setting parameters!")
        pass

    def clear_grid(self):   
        for row_entries in self.entries:
            for entry in row_entries:
                entry.config(state='normal')
                entry.delete(0, tk.END)  # Töröljük a cellák tartalmát
        Board.clear()

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

    def start_simulation(self):
        # Új szál indítása az asyncio eseményciklushoz
        threading.Thread(target=lambda: asyncio.run(self.run_simulation()), daemon=True).start()

    async def run_simulation(self):
        # Kiindulási állapotok
        messagebox.showinfo("Solve", "Solving Sudoku!")
        Population.individuals = []
        Population.generation = 1
        GA.solved = ""
        GA.restarted = 0
        GA.running = True

        # Inicializálás
        Population.initialization(Parameters.population_size)

        while Population.generation != Parameters.max_generation and GA.running:
            # Ha beragadtunk, újrainicializálás
            if GA.stucked == Parameters.restart_after_stuck_gen:
                Population.re_initialization(Parameters.reborn_rate)

            # Fitness érték számítása
            GA.fitness(Population.individuals)

            # Ellenőrizzük, hogy valamelyik egyed elérte-e a maximális fitness értéket
            if Population.individuals[-1].fitness == 243:  # Sudoku esetében a maximum fitness érték
                GA.solved = "true"
                break

            # Egyedek rendezése, szelekció, keresztezés és mutáció
            Population.sort()

            # Kiírás: Generáció száma, legjobb és legrosszabb fitness
            fittest = [ind.fitness for ind in Population.individuals[-10:]]
            worst = [ind.fitness for ind in Population.individuals[:10]]
            print(f"Generation: {Population.generation}/{Parameters.max_generation}  Fittest: {max(fittest)}  Worst: {min(worst)}")

            GA.selection(Population.individuals, Parameters.selection_rate)
            GA.crossover(
                Population.individuals,
                Parameters.selection_rate,
                Parameters.crossover_type
            )
            GA.mutation(
                Population.individuals,
                Parameters.mutation_rate,
                Parameters.mutation_strength,
                Parameters.mutation_type
            )

            # Generációk növelése
            Population.generation += 1
            Population.show_best()

            # Aszinkron késleltetés (pl. vizualizáció frissítésére)
            await asyncio.sleep(0)

        # Eredmény ellenőrzése
        if Population.individuals[-1].fitness != 243:
            GA.solved = "false"
        GA.fitness(Population.individuals)
        GA.running = False


        # Eredmény ellenőrzése
        if Population.individuals[-1].fitness != 243:
            GA.solved = "false"
        GA.fitness(Population.individuals)
        GA.running = False
        # Itt hívhatod meg a canvas frissítését vagy más vizualizációt
        
    def update_cell(self, row, col, value):
        """ Frissíti az adott cellát a Sudoku táblán. """
        self.entries[row][col].delete(0, tk.END)
        self.entries[row][col].insert(0, str(value))
        self.root.update_idletasks() 
    
    def stop_running(self):
        GA.running = False


    def draw_parameter_frame(self):
        """ Paraméterek megadására szolgáló keret létrehozása """
        self.parameter_frame = tk.Frame(self.main_frame, bg="#333333", pady=10)
        self.parameter_frame.pack(fill=tk.BOTH)

        labels = [
            "restart_after_stuck_gen",
            "given_numbers",
            "max_generation",
            "population_size",
            "selection_rate",
            "selection_type",
            "crossover_type",
            "mutation_rate",
            "mutation_strength",
            "mutation_type",
        ]

        self.parameter_entries = {}
        for i, label in enumerate(labels):
            tk.Label(
                self.parameter_frame,
                text=label,
                fg="white",
                bg="#333333",
                font=("Arial", 10),
            ).grid(row=i, column=0, sticky="w", padx=5, pady=2)

            entry = tk.Entry(self.parameter_frame, font=("Arial", 10), width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.parameter_entries[label] = entry

        # Save gomb
        save_button = tk.Button(
            self.parameter_frame,
            text="Save Parameters",
            command=self.save_parameters,
            bg="#555555",
            fg="white",
            font=("Arial", 12),
        )
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)
        self.load_default_parameters()

    def save_parameters(self):
        """ A paraméterek mentése a Parameters osztályba """
        try:
            Parameters.restart_after_stuck_gen = int(self.parameter_entries["restart_after_stuck_gen"].get())
            Parameters.given_numbers = int(self.parameter_entries["given_numbers"].get())
            Parameters.max_generation = int(self.parameter_entries["max_generation"].get())
            Parameters.population_size = int(self.parameter_entries["population_size"].get())
            Parameters.selection_rate = float(self.parameter_entries["selection_rate"].get())
            Parameters.selection_type = self.parameter_entries["selection_type"].get()
            Parameters.crossover_type = self.parameter_entries["crossover_type"].get()
            Parameters.mutation_rate = float(self.parameter_entries["mutation_rate"].get())
            Parameters.mutation_strength = float(self.parameter_entries["mutation_strength"].get())
            Parameters.mutation_type = self.parameter_entries["mutation_type"].get()

            messagebox.showinfo("Success", "Parameters saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameter value: {e}")

    def load_default_parameters(self):
        """Betölti a Parameters osztály alapértelmezett értékeit az input mezőkbe."""
        for key, entry in self.parameter_entries.items():
            value = getattr(Parameters, key, "")  # Megpróbáljuk lekérni az értéket
            entry.insert(0, str(value))  # Az értéket szöveggé alakítva beírjuk

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
