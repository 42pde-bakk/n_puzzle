import sys
import copy
import numpy as np
from srcs.gamestate import Gamestate, Direction
from srcs.puzzle import Puzzle, to_spiralarray


def is_even(nb: int) -> bool:
	return nb % 2 == 0


def is_odd(nb: int) -> bool:
	return not is_even(nb)


class PuzzleValidator:
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
		inversion_count = 0
		spiral_arr = to_spiralarray(puzzle.original_position).flatten()
		tiles_nb = puzzle.size * puzzle.size
		for i in range(0, tiles_nb - 1):
			for j in range(i + 1, tiles_nb):
				if spiral_arr[i] > spiral_arr[j]:
					# print(f'inversion, cus spiral_arr[{i}]={spiral_arr[i]} > spiral_arr[{j}]={spiral_arr[j]}')
					inversion_count += 1
		zero_pos = puzzle.find_zero_pos()
		print(f'inversion_count is {inversion_count}, position from bottom is {puzzle.size - zero_pos[0]}')
		if is_odd(puzzle.size) and is_even(inversion_count):
			return True
		elif is_even(puzzle.size) and (is_even(puzzle.size - zero_pos[0]) ^ is_odd(inversion_count)):
			# the ^ operator is a XOR gate
			return True
		return False

	@staticmethod
	def check_solution(original_puzzle: Puzzle, move_sequence: list[Direction]):
		gamestate = Gamestate()
		gamestate.rows = copy.deepcopy(original_puzzle.original_position)
		gamestate.size = original_puzzle.size
		gamestate.zero_pos = gamestate.find_zero_pos()

		for move in move_sequence:
			gamestate.do_move(Direction(move))
		print(f'is valid solution: {np.array_equal(original_puzzle.goal_matrix, gamestate.rows)}')
