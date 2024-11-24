import random
import logging
from Individual import Individual 
from Board import Board


class Population:
    fittest = 0
    generation = 1
    individuals = []

    @staticmethod
    def initialization(n):
        # Initialize population  n individuals
        for i in range(1, n+1):
            individual = Individual()
            individual.id = i

            # Fill with given genoms and randoms
            for row in range(9):
                for col in range(9):
                    if Board.problem[row][col] > 0:
                        individual.body[row][col] = Board.problem[row][col]
                    else:
                        individual.body[row][col] = random.randint(1, 9)

            Population.individuals.append(individual)
        logging.info(f'{len(Population.individuals)} individuals created')

    @staticmethod
    def get_best():
        # Show the body and genome of the fittest individual
        best_individual = Population.individuals[-1]
        for i in range(9):
            for j in range(9):
                Board.individualBody[i][j] = best_individual.body[i][j]
                Board.individualGenomValues[i][j] = best_individual.genomeValues[i][j]
        return best_individual


    @staticmethod
    def show_one(index):
        # Show the body and genome of a specific individual
        individual = Population.individuals[index - 1]
        for i in range(9):
            for j in range(9):
                Board.individualBody[i][j] = individual.body[i][j]
                Board.individualGenomValues[i][j] = individual.genomeValues[i][j]

    @staticmethod
    def sort():
        from GA import GA
        # Sort the population by fitness
        Population.individuals.sort(key=lambda individual: individual.fitness)
        best_individual = Population.individuals[-1]
        logging.info(f"Fittest: {best_individual.id} fitness value: {best_individual.fitness}")

        if best_individual.fitness > Population.fittest:
            GA.stucked = 0
            logging.debug("stucked = 0")
            Population.fittest = best_individual.fitness
        else:
            GA.stucked += 1
            logging.debug(f"stucked++ (stucked = {GA.stucked})")

    @staticmethod
    def re_initialization(reborn_rate):
        from GA import GA
        # Reinitialize a portion of the population
        n = int(len(Population.individuals) * reborn_rate)
        GA.stucked = 0
        GA.restarted += 1

        logging.debug(f"Reborn n = {n}")

        for i in range(n):
            for row in range(9):
                for col in range(9):
                    if Board.problem[row][col] > 0:
                        Population.individuals[i].body[row][col] = Board.problem[row][col]
                    else:
                        Population.individuals[i].body[row][col] = random.randint(1, 9)
