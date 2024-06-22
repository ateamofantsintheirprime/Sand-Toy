from pprint import pprint
from copy import copy, deepcopy
from itertools import product
import numpy
dict = {}


def generate_combinations():
	# Generate all combinations of 9 elements of 0s and 1s
	combinations = product([0, 1], repeat=9)
	
	# Convert the flat lists into 3x3 matrices
	matrices = []
	for comb in combinations:
		matrix = [list(comb[i:i+3]) for i in range(0, 9, 3)]
		matrices.append(matrix)
	
	return matrices

def print_matrix(matrix):
	# Print the matrix in a readable format
	# for row in numpy.transpose(matrix).tolist():
	for row in matrix:
		print(' '.join(map(str, row)))
	print()

def fall_down(input):
	matrix = deepcopy(input)
	# Iterate over the columns
	for col in range(3):
		# For each column, start from the second-to-last row and move upwards
		for row in range(1, -1, -1):
			# If the current cell is 1 and the cell below is 0, swap them
			if matrix[row][col] == 1 and matrix[row + 1][col] == 0:
				matrix[row][col], matrix[row + 1][col] = matrix[row + 1][col], matrix[row][col]
	return matrix

def can_fall_down(matrix):
	# Iterate over the columns
	for col in range(3):
		# For each column, start from the second-to-last row and move upwards
		for row in range(2):
			# Check if the current cell is 1 and the cell below is 0
			if matrix[row][col] == 1 and matrix[row + 1][col] == 0:
				# print("can fall down")
				# print_matrix(matrix)
				# print(row,col)
				return True
	return False

def has_stack_of_1s_next_to_zeros(matrix):
    # Iterate over the columns
    for col in range(3):
        for row in range(2):  # Check rows 0 and 1 for stacks
            # Check for a vertical stack of two 1s
            if matrix[row][col] == 1 and matrix[row + 1][col] == 1:
                # Check if there are two zeros next to the stack (left or right)
                if col > 0 and matrix[row][col - 1] == 0 and matrix[row + 1][col - 1] == 0:
                    return True
                if col < 2 and matrix[row][col + 1] == 0 and matrix[row + 1][col + 1] == 0:
                    return True
    return False
combinations = generate_combinations()

solved = 0
solved_combinations = []
unsolved_combinations = []
for square in combinations:

	solution = fall_down(square)
	if not has_stack_of_1s_next_to_zeros(solution):
		solved +=1 
		solved_combinations.append([square,solution])
	else:
		# print("stack of 1s:")
		# print_matrix(square)
		# print("unsolved:")
		# print_transpose(square)
		unsolved_combinations.append([square, solution])

print("UNSOLVED!!")
for pair in unsolved_combinations:
	# print("initial:")
	# print_matrix(pair[0])
	print("fallen:")
	print_matrix(pair[1])
	print()
print()
print("SOLVED!!")
for pair in solved_combinations:
	print("initial:")
	print_matrix(pair[0])
	print("solved:")
	print_matrix(pair[1])
	print()
print()

print("unsolved: ", len(unsolved_combinations))
print("solved: ", solved)
