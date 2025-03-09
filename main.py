import copy
import random

LETTER = ['A', 'B', 'C', 'D']

def initialize_population(population_size, grid):
    population = []
    letter = set(LETTER)  # Define the complete set of letters

    for _ in range(population_size):
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


def crossover(parent1, parent2):
    """Crossover between parent1 and parent2"""
    crossover_point = random.randint(1,3)
    child = copy.deepcopy(parent1)

    """Swap the entire row to ensure row validity"""
    for i in range(crossover_point,4):
        """From the crossover_point row to the last row"""
        for j in range(4):
            """Swap all four columns values"""""
            child[i][j]= parent2[i][j]
    return child

def mutation(grid, initial_grid):
    """Mutate by shifting entire rows left or right,  only if it doesn't introduce conflicts."""
    mutation_rate = 1 # Increase rate for testing (can be adjusted)
    for row in range(4):
        if random.random() < mutation_rate:
            blank_positions = [col for col in range(4) if initial_grid[row][col] == '']

            if blank_positions:  # Only mutate if empty spots exist
                shift_direction = random.choice(["left", "right"])
                temp_grid = [r[:] for r in grid]  # Copy grid for simulation

                if shift_direction == "left":
                    temp_grid[row] = temp_grid[row][1:] + [temp_grid[row][0]]
                else:
                    temp_grid[row] = [temp_grid[row][-1]] + temp_grid[row][:-1]

                # Check if mutation breaks constraints
                if fitness(temp_grid) <= fitness(grid):  # Apply only if it improves or maintains fitness
                    grid[row] = temp_grid[row]

    return grid


"""Main Genetic Algorithm Function"""
def genetic_algorithm(population_size,tournament_size, initial_grid, max_generations):
    # prepare initial population
    population = initialize_population(population_size, initial_grid)
    solutions={}

    for generation in range(1, max_generations+1):
        population.sort(key=fitness)

        for individual in population:
            if fitness(individual) == 0:
                solution_tuple = tuple(map(tuple, individual))
                if solution_tuple not in solutions:
                    solutions[solution_tuple] = generation

        if solutions and len(solutions) >= 5:
            break

        # Keep the top 5 (elitism) to ensure best solutions are not lost
        new_population = population[:5]

        # Generate new individuals to maintain population size
        while len(new_population) < population_size:
            parent1, parent2 = parent_selection(population, tournament_size)
            child = crossover(parent1, parent2)
            mutated_child = mutation(child, initial_grid)
            new_population.append(mutated_child)

        population = new_population

        # Print progress for monitoring
        if generation % 50 == 0:
            # Print best fitness in current generation
            best_dup = fitness(population[0])
            print(f"Generation {generation}: Best fitness = {best_dup}")

    return [(list(map(list, sol)), gen) for sol, gen in
            solutions.items()] if solutions else "No solution found, reached the max generation"


# Example usage


def print_grid(grid):
    for row in grid:
        print(" ".join(row))


initial_grid = [['C', '', '', 'D'],
                ['', '', 'A', ''],
                ['', '', '', ''],
                ['D', '', '', 'A']]

solutions = genetic_algorithm(population_size=20, tournament_size=3, initial_grid=initial_grid, max_generations=500)
if isinstance(solutions, str):
    print(solutions)
else:
    print("Solutions found:")
    for idx, (sol, gen) in enumerate(solutions, 1):
        print(f"Solution {idx} (Found at Generation {gen}):")
        print_grid(sol)
        print()






