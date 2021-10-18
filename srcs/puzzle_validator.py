from srcs.npuzzle import Npuzzle
import sys


def is_even(nb: int) -> bool:
	return nb % 2 == 0


def is_odd(nb: int) -> bool:
	return not is_even(nb)


class PuzzleValidator:
	def __init__(self):
		pass

	@staticmethod
	def is_valid(puzzle: Npuzzle) -> bool:
		"""Assert all rows are equal in length and without duplicate items"""
		if puzzle.size != puzzle.rows.shape[0] or puzzle.size != puzzle.rows.shape[1]:
			print('Error\nThe puzzle is not the size you say it is!', file=sys.stderr)
			return False
		puzzle_as_set = set(puzzle.rows.flatten())
		if len(puzzle_as_set) != puzzle.size ** 2:
			print('Error\nThis puzzle has duplicates!', file=sys.stderr)
			return False
		if not all(x in range(0, puzzle.size ** 2) for x in puzzle_as_set):
			print(f'Error\nPlease make sure all numbers in the puzzle are between 0 and {puzzle.size ** 2 - 1}')
			return False
		return True

	@staticmethod
	def is_solvable(puzzle: Npuzzle) -> bool:
		"""Checks whether the puzzle actually is solvable"""
		flattened_puzzle = list(puzzle.rows.flatten())
		inversion_count = 0
		for i in range(0, puzzle.size ** 2 - 1):
			for j in range(i + 1, puzzle.size ** 2):
				if flattened_puzzle[i] > flattened_puzzle[j] != 0 and flattened_puzzle[i] != 0:
					inversion_count += 1
		if is_odd(puzzle.size) and is_even(inversion_count):
			return True
		elif is_even(puzzle.size) and (is_even(puzzle.size - puzzle.zero_pos[0]) ^ is_odd(inversion_count)):
			# the ^ operator is a XOR gate
			return True
		return False
