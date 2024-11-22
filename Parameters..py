class Parameters:
    reborn_rate = 0.5  # if stuck
    restart_after_stuck_gen = 20
    given_numbers = 40
    max_generation = 10000
    population_size = 3000
    selection_rate = 0.25
    selection_type = "tournament"  # random - tournament 2 from 4 parent
    crossover_type = "grid"  # grid - rows - columns
    mutation_rate = 0.7  # how many child will be mutated
    mutation_strength = 1  # how many genoms will be mutated
    mutation_type = "rand"  # swap - big random small swap - increment - random
