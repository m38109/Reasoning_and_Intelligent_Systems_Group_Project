import copy
import random


LETTER = ['A', 'B', 'C', 'D']

def initialize_population(size, grid):
    population = []
    letter = set(LETTER)  # Define the complete set of letters

    for _ in range(size):
        new_grid = copy.deepcopy(grid)

        for row in new_grid:
            existing_letters = set(row) - {' '} # Get existing letters in the row
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







    return count_conflicts



initial_grid = [['B', '', '', ''],
                ['', '', '', ''],
                ['', 'B', '', ''],
                ['A', '', '', 'B']]

populations = initialize_population(3, initial_grid)
populations_with_conflicts = []
for idx, pop in enumerate(populations):
    row_conflicts = count_row_conflicts(pop)
    column_conflicts = count_column_conflicts(pop)
    populations_with_conflicts.append((idx + 1, pop, row_conflicts, column_conflicts))

# Display results
output_data = []
for pop_id, pop, row_conflicts, column_conflicts in populations_with_conflicts:
    output_data.append({"Population": pop_id, "Row Conflicts": row_conflicts, "Column Conflicts": column_conflicts, "Population:": pop})

if output_data:
    for row in output_data:
        print(row)
