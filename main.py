import copy
import random


LETTER = ['A', 'B', 'C', 'D']

def initialize_population(size, grid):
    population = []
    letter = set(LETTER)  # Define the complete set of letters

    for _ in range(size):
        new_grid = copy.deepcopy(grid)

        for row in new_grid:
            existing_letters = set(row) - {''} # Get existing letters in the row
            missing_letters = list(letter - existing_letters)  # Find missing letters
            random.shuffle(missing_letters)  # Shuffle missing letters randomly

            for i in range(len(row)):
                if row[i] == '' and missing_letters:  # Fill empty cells if missing letters exist
                    row[i] = missing_letters.pop()

        population.append(new_grid)

    return population


def fitness(grid):
    """Compute the number of duplicate letters in columns, row and sub-gird (lower is better)"""
    return count_row_conflicts(grid) + count_column_conflicts(grid) + count_subgrid_conflicts(grid)

def count_row_conflicts(grid):
    """Compute the number of row conflicts"""
    count_conflicts = 0
    for row in grid:
        letter_counts = {}  # Dictionary to count letter occurrences
        for letter in row:
            if letter:  # Ignore empty cells
                if letter in letter_counts:
                    count_conflicts += 1  # Increase conflict count for duplicates
                else:
                    letter_counts[letter] = 1  # First occurrence of letter
    return count_conflicts

def count_column_conflicts(grid):
    """Compute the number of column conflicts"""
    count_conflicts = 0
    for col in range(4):
        letter_counts = {}
        for row in grid:
            letter = row[col]
            if letter:
                if letter in letter_counts:
                    count_conflicts += 1
                else:
                    letter_counts[letter] = 1
    return count_conflicts

def count_subgrid_conflicts(grid):
    """Compute the number of subgrid conflicts"""
    count_conflicts = 0
    subgrid_size = 2

    for start_row in [0,2]:
        for start_col in [0,2]:
            letter_counts = {}

            for i in range(start_row,start_row+subgrid_size):
                for j in range(start_col,start_col+subgrid_size):
                    letter = grid[i][j]
                    if letter:
                        if letter in letter_counts:
                            count_conflicts += 1
                        else:
                            letter_counts[letter] = 1
    return count_conflicts

#select parents with tournament method
def tournament_selection(population, tournament_size):
    best_individual = None
    best_fitness = float('inf') # the best solution is the one with the lowest fitness

    for _ in range(tournament_size):
        candidate = random.choice(population)
        candidate_fitness = fitness(candidate)
        if candidate_fitness < best_fitness:
            best_individual = candidate
            best_fitness = candidate_fitness
    return best_individual

def parent_selection(population, tournament_size):
    """Select different individual as parents"""
    parent1 = tournament_selection(population, tournament_size)

    while True:
        parent2 = tournament_selection(population, tournament_size)
        if parent2 != parent1:
            break
    return parent1, parent2


def crossover(parent1, parent2, initial_grid):
    """Crossover between two parents """
    crossover_point = random.randint(1,3)
    child = copy.deepcopy(parent1)

    for i in range(crossover_point,4):
        for j in range(4):
            if initial_grid[i][j] == ' ':
                child[i][j]= parent2[i][j]
    return child






