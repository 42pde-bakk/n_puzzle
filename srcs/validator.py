import sys
import numpy as np
from puzzle import Puzzle
from utils.util_functions import find_pos_in_array


def count_inversions(puzzle: Puzzle) -> int:
	"""Return the amount of inversions in the puzzle"""
	inversions = 0
	for a in range(puzzle.size ** 2 - 1):
		for b in range(a + 1, puzzle.size ** 2):
			# Get the values of the a-th and b-th values in the original array
			a_val = puzzle.original_position[a // puzzle.size][a % puzzle.size]
			b_val = puzzle.original_position[b // puzzle.size][b % puzzle.size]
			if np.where(puzzle.goal_matrix == a_val) > np.where(puzzle.goal_matrix == b_val):
				inversions += 1
	return inversions


class PuzzleValidator:
	"""Utility class to check if a puzzle is valid and solvable"""

	def __init__(self):
		pass

	@staticmethod
	def is_valid(puzzle: Puzzle) -> bool:
		"""Assert all rows are equal in length and without duplicate items"""
		if puzzle.size != puzzle.original_position.shape[0] or puzzle.size != puzzle.original_position.shape[1]:
			print('Error\nThe puzzle is not the size you say it is!', file=sys.stderr)
			return False
		puzzle_as_set = set(puzzle.original_position.flatten())
		if len(puzzle_as_set) != puzzle.size ** 2:
			print('Error\nThis puzzle has duplicates!', file=sys.stderr)
			return False
		if not all(x in range(0, puzzle.size ** 2) for x in puzzle_as_set):
			print(f'Error\nPlease make sure all numbers in the puzzle are between 0 and {puzzle.size ** 2 - 1}')
			return False
		return True

	@staticmethod
	def is_solvable(puzzle: Puzzle) -> bool:
		"""Checks whether the puzzle actually is solvable"""

		inversion_count = count_inversions(puzzle)
		og_zeropos = find_pos_in_array(puzzle.original_position)
		goal_zeropos = find_pos_in_array(puzzle.goal_matrix)
		emptytile_distance = abs(og_zeropos[0] - goal_zeropos[0]) + abs(og_zeropos[1] - goal_zeropos[1])
		return emptytile_distance % 2 == inversion_count % 2
