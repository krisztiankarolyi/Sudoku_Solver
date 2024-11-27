import random
from Parameters import Parameters
from Problems import Problems
import tkinter as tk

class Board:
    problem = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    individualBody = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    individualGenomValues = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    @staticmethod
    def clear():
        for i in range(9):
            for j in range(9):
                Board.problem[i][j] = 0
                Board.individualBody[i][j] = 0
                Board.individualGenomValues[i][j] = 0

    @staticmethod
    def set_problem(given_numbers: int):
        Board.clear()
        random_choice = random.choice([1, 2])
        for i in range(9):
            for j in range(9):
                if random_choice == 1:
                    Board.problem[i][j] = Problems.solved1[i][j]
                else:
                    Board.problem[i][j] = Problems.solved1[i][j]

        # remove numbers
        n = 81 - given_numbers
        while n != 0:
            rand_x = random.randint(0, 8)
            rand_y = random.randint(0, 8)
            if Board.problem[rand_x][rand_y] != 0:
                Board.problem[rand_x][rand_y] = 0
                n -= 1
    
    @staticmethod
    def read_problem(app):
        given_numbers = 0
        for i in range(9):
            for j in range(9):
                value = app.entries[i][j].get().strip()  # Beolvassuk az értéket a cellából
                if value.isdigit():  # Csak akkor vesszük figyelembe, ha szám
                    Board.problem[i][j] = int(value[0])
                    app.entries[i][j].delete(0, tk.END)  # Töröljük a mező tartalmát
                    app.entries[i][j].insert(0, value[0])  # Beszúrjuk az első számjegyet
                    given_numbers+=1
                    
                else:
                    Board.problem[i][j] = 0  # Ha üres vagy nem szám, akkor 0 lesz
        print("The problem was read from the board")
        print(Board.problem)
        Parameters.given_numbers = given_numbers
        app.parameter_entries["given_numbers"].delete(0, tk.END)
        app.parameter_entries["given_numbers"].insert(0, given_numbers) 

