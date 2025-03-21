import copy
import random

# Define grid and subgrid sizes dynamically
GRID_SIZE = 4
SUBGRID_SIZE = 2
LETTER = ['A', 'B', 'C', 'D']  # Can be made dynamic if needed

# Generate initial population of candidate grids
# Each row gets filled with the missing letters in random order
# This ensures that rows are always valid

def initialize_population(size, grid):
    population = []
    for _ in range(size):
        new_grid = copy.deepcopy(grid)
        for row in new_grid:
            existing_letters = [cell for cell in row if cell != '']
            missing_letters = [letter for letter in LETTER if letter not in existing_letters]
            empty_indices = [i for i, cell in enumerate(row) if cell == '']
            random.shuffle(missing_letters)
            for i, index in enumerate(empty_indices):
                if i < len(missing_letters):
                    row[index] = missing_letters[i]
        population.append(new_grid)
    return population

# Compute the number of duplicate letters in columns, row and sub-grid (lower is better)
def fitness(grid):
    return count_row_conflicts(grid) + count_column_conflicts(grid) + count_subgrid_conflicts(grid)

# Compute the number of row conflicts
def count_row_conflicts(grid):
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

# Compute the number of column conflicts
def count_column_conflicts(grid):
    count_conflicts = 0
    for col in range(GRID_SIZE):
        letter_counts = {}
        for row in grid:
            letter = row[col]
            if letter:
                if letter in letter_counts:
                    count_conflicts += 1
                else:
                    letter_counts[letter] = 1
    return count_conflicts

# Compute the number of subgrid conflicts
def count_subgrid_conflicts(grid):
    count_conflicts = 0
    for start_row in range(0, GRID_SIZE, SUBGRID_SIZE):
        for start_col in range(0, GRID_SIZE, SUBGRID_SIZE):
            letter_counts = {}
            for i in range(start_row, start_row + SUBGRID_SIZE):
                for j in range(start_col, start_col + SUBGRID_SIZE):
                    letter = grid[i][j]
                    if letter:
                        if letter in letter_counts:
                            count_conflicts += 1
                        else:
                            letter_counts[letter] = 1
    return count_conflicts

# Select the best individual among randomly chosen subset of the population
def tournament_selection(population, tournament_size):
    best_individual = None
    best_fitness = float('inf')  # the best solution is the one with the lowest fitness

    for _ in range(tournament_size):
        candidate = random.choice(population)
        candidate_fitness = fitness(candidate)
        if candidate_fitness < best_fitness:
            best_individual = candidate
            best_fitness = candidate_fitness
    return best_individual

# Select two different individuals using tournament selection
def parent_selection(population, tournament_size):
    parent1 = tournament_selection(population, tournament_size)

    while True:
        parent2 = tournament_selection(population, tournament_size)
        if parent2 != parent1:
            break
    return parent1, parent2

# Crossover between parent1 and parent2 by swapping entire rows
# to ensure row validity is preserved
def crossover(parent1, parent2):
    crossover_point = random.randint(1, GRID_SIZE - 1)
    child = copy.deepcopy(parent1)

    for i in range(crossover_point, GRID_SIZE):
        for j in range(GRID_SIZE):
            child[i][j] = parent2[i][j]
    return child

# Mutate by shifting entire rows left or right, only if it doesn't introduce conflicts
def mutation(grid, initial_grid):
    mutation_rate = 1  # Increase rate for testing (can be adjusted)
    for row in range(GRID_SIZE):
        if random.random() < mutation_rate:
            blank_positions = [col for col in range(GRID_SIZE) if initial_grid[row][col] == '']

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

# Main Genetic Algorithm Function
def genetic_algorithm(population_size, tournament_size, initial_grid, max_generations):
    # prepare initial population
    population = initialize_population(population_size, initial_grid)
    solutions = {}

    for generation in range(1, max_generations + 1):
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

    return [(list(map(list, sol)), gen) for sol, gen in solutions.items()] if solutions else "No solution found, reached the max generation"

# Print solution grid
def print_grid(grid):
    for row in grid:
        print(" ".join(row))

# Define initial grid
initial_grid = [['C', '', '', 'D'],
                ['', '', 'A', ''],
                ['', '', '', ''],
                ['D', '', '', 'A']]

# Run the algorithm
solutions = genetic_algorithm(population_size=20, tournament_size=3, initial_grid=initial_grid, max_generations=500)
if isinstance(solutions, str):
    print(solutions)
else:
    print("Solutions found:")
    for idx, (sol, gen) in enumerate(solutions, 1):
        print(f"Solution {idx} (Found at Generation {gen}):")
        print_grid(sol)
        print()