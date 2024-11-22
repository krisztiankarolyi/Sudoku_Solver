import random

import Board

class GA:
    running = False
    solved = ""
    stucked = 0
    restarted = 0

    @staticmethod
    def fitness(individuals):
        for individual in individuals:
            for i in range(9):
                for j in range(9):
                    individual.genomeValues[i][j] = GA.genome_value(i, j, individual.body[i][j], individual)
            individual.set_fitness()

    @staticmethod
    def crossover(individuals, percentage, type_):
        n = int(len(Population.individuals) * percentage)

        for i in range(0, n, 2):
            parentA, parentB, parentC, parentD = 0, 0, 0, 0

            # selection type
            if Parameters.selection_type == "random":
                # select 2 random
                parentA = random.randint(n, len(Population.individuals) - 1)
                parentB = random.randint(n, len(Population.individuals) - 1)
                while parentA == parentB:
                    parentA = random.randint(n, len(Population.individuals) - 1)
                    parentB = random.randint(n, len(Population.individuals) - 1)
            elif Parameters.selection_type == "tournament":
                parentA = random.randint(n, len(Population.individuals) - 1)
                parentB = random.randint(n, len(Population.individuals) - 1)
                parentC = random.randint(n, len(Population.individuals) - 1)
                parentD = random.randint(n, len(Population.individuals) - 1)
                while len(set([parentA, parentB, parentC, parentD])) < 4:
                    parentA = random.randint(n, len(Population.individuals) - 1)
                    parentB = random.randint(n, len(Population.individuals) - 1)
                    parentC = random.randint(n, len(Population.individuals) - 1)
                    parentD = random.randint(n, len(Population.individuals) - 1)

                # only two survive
                parentA = parentA if individuals[parentA].fitness >= individuals[parentC].fitness else parentC
                parentB = parentB if individuals[parentB].fitness >= individuals[parentD].fitness else parentD

            # create new child
            if type_ == "row":
                for j in range(9):
                    for k in range(9):
                        individuals[i].body[j][k] = individuals[parentA].body[j][k] if j % 2 == 0 else individuals[parentB].body[j][k]
            elif type_ == "col":
                for j in range(9):
                    for k in range(9):
                        individuals[i].body[j][k] = individuals[parentA].body[j][k] if k % 2 == 0 else individuals[parentB].body[j][k]
            elif type_ == "grid":
                for ii in range(0, 9, 3):
                    for jj in range(0, 9, 3):
                        randParent = parentA if random.randint(0, 1) == 1 else parentB
                        for iii in range(3):
                            for jjj in range(3):
                                individuals[i].body[ii + iii][jj + jjj] = individuals[randParent].body[ii + iii][jj + jjj]
                                if randParent == parentA:
                                    individuals[i + 1].body[ii + iii][jj + jjj] = individuals[parentB].body[ii + iii][jj + jjj]

    @staticmethod
    def selection(individuals, percentage):
        n = int(len(Population.individuals) * percentage)
        for i in range(n):
            individuals[i].kill()

    @staticmethod
    def mutation(individuals, rate, strength, type_):
        n = int(Parameters.population_size * Parameters.selection_rate * rate)
        for i in range(n):
            counter = 0
            while counter < strength:
                x = random.randint(0, 8)
                y = random.randint(0, 8)

                if type_ == "incr":
                    if Board.problem[x][y] == 0:
                        if individuals[i].body[x][y] == 9:
                            individuals[i].body[x][y] = 1
                        else:
                            individuals[i].body[x][y] += 1
                        counter += 1
                elif type_ == "swap small":
                    iPush = random.randint(0, 2)
                    jPush = random.randint(0, 2)

                    x1, y1 = random.randint(0, 2), random.randint(0, 2)
                    x2, y2 = random.randint(0, 2), random.randint(0, 2)

                    if Board.problem[x1 + (iPush * 3)][y1 + (jPush * 3)] == 0 and Board.problem[x2 + (iPush * 3)][y2 + (jPush * 3)] == 0:
                        Board.problem[x1 + (iPush * 3)][y1 + (jPush * 3)], Board.problem[x2 + (iPush * 3)][y2 + (jPush * 3)] = Board.problem[x2 + (iPush * 3)][y2 + (jPush * 3)], Board.problem[x1 + (iPush * 3)][y1 + (jPush * 3)]
                        counter += 1
                elif type_ == "rand":
                    if Board.problem[x][y] == 0:
                        individuals[i].body[x][y] = random.randint(1, 9)
                        counter += 1
                elif type_ == "swap big":
                    while individuals[i].genomeValues[x][y] == 3:
                        x = random.randint(0, 8)
                        y = random.randint(0, 8)

                    if Board.problem[x][y] == 0:
                        individuals[i].body[x][y] = random.randint(1, 9)
                        counter += 1

    @staticmethod
    def genome_value(x, y, num, individual):
        rowOk, columnOk, gridOk = True, True, True

        # check column
        for i in range(9):
            if individual.body[i][y] == num and x != i:
                columnOk = False
                break
        # check row
        for j in range(9):
            if individual.body[x][j] == num and y != j:
                rowOk = False
                break

        # check small matrix
        iPush, jPush = 0, 0
        if x > 2: iPush += 3
        if x > 5: iPush += 3
        if y > 2: jPush += 3
        if y > 5: jPush += 3

        for i in range(3):
            for j in range(3):
                if individual.body[i + iPush][j + jPush] == num and (i + iPush != x or j + jPush != y):
                    gridOk = False
                    break

        genomeValue = 0
        if rowOk: genomeValue += 1
        if columnOk: genomeValue += 1
        if gridOk: genomeValue += 1

        return genomeValue

    @staticmethod
    def genome_value2(x, y, num, individual):
        for i in range(9):
            if individual.body[i][y] == num and x != i:
                return 0
        for j in range(9):
            if individual.body[x][j] == num and y != j:
                return 0

        iPush, jPush = 0, 0
        if x > 2: iPush += 3
        if x > 5: iPush += 3
        if y > 2: jPush += 3
        if y > 5: jPush += 3

        for i in range(3):
            for j in range(3):
                if individual.body[i + iPush][j + jPush] == num and (i + iPush != x or j + jPush != y):
                    return 0
        return 1
