import copy
from typing import List
import numpy as np
import os
import sys
# import tty
# import termios
# from msvcrt import getch
from utils.util_functions import find_pos_in_array, get_keypress
from gamestate import Gamestate, Direction
from generate_puzzle import make_puzzle


# Create a spiral matrix from a given list
def to_spiralarray(arr: np.ndarray) -> np.ndarray:
	"""Return a np matrix containing the matrix, but in spiral form starting topleft moving clockwise"""
	m, n = arr.shape
	arr = arr.flatten()

	top = left = 0
	bottom = m - 1
	right = n - 1

	# construct an `M × N` matrix
	mat = [[0 for _ in range(n)] for _ in range(m)]
	index = 0

	while True:
		if left > right:
			break

		# print top row
		for i in range(left, right + 1):
			mat[top][i] = arr[index]
			index += 1
		top += 1

		if top > bottom:
			break

		# print right column
		for i in range(top, bottom + 1):
			mat[i][right] = arr[index]
			index += 1
		right -= 1

		if left > right:
			break

		# print bottom row
		for i in range(right, left - 1, -1):
			mat[bottom][i] = arr[index]
			index += 1
		bottom -= 1

		if top > bottom:
			break

		# print left column
		for i in range(bottom, top - 1, -1):
			mat[i][left] = arr[index]
			index += 1
		left += 1

	return np.array(mat, dtype=np.uint16)


class Puzzle:
	"""Class to contain a puzzle's size, starting position and the goal positions"""
	def __init__(self):
		self.size = 0
		self.goal_matrix = np.ndarray
		self.original_position = np.ndarray

	# noinspection PyTypeChecker
	def set_goals(self):
		"""Create the goal matrix"""
		self.goal_matrix = \
			to_spiralarray(
				np.array(list(range(1, self.size ** 2)) + [0], dtype=np.uint16).reshape((self.size, self.size))
			)

	def create_starting_state(self) -> Gamestate:
		"""Copy original position to a Gamestate class instance"""
		gamestate = Gamestate()
		gamestate.rows = copy.deepcopy(self.original_position)
		Gamestate.size = self.size
		# noinspection PyTypeChecker
		gamestate.zero_pos = find_pos_in_array(gamestate.rows)[::-1]  # Inverting so it's (x, y) instead of (y, x)
		return gamestate

	def create_reverse_puzzle(self):
		reverse = Puzzle()
		reverse.size = self.size
		reverse.goal_matrix = self.original_position.copy()
		reverse.original_position = self.goal_matrix.copy()
		return reverse

	def readrows(self, rows: List[str]) -> np.ndarray:
		"""Create np array containing all the rows"""
		ints = []
		for row in rows:
			ints += [int(token) for token in row.split('#')[0].split()]
		self.size = ints.pop(0)
		return np.array(ints, dtype=np.uint16).reshape((self.size, self.size))

	def parse_puzzle(self, rows: List[str]):
		"""Parse puzzle, don't validate yet"""
		self.size = 0
		self.original_position = self.readrows(rows)
		self.set_goals()

	def create_random_state(self):
		size = input(f'Dear {os.environ["USER"]}, what size do you want your puzzle to be? ')
		try:
			size = int(size)
		except ValueError:
			print(f'Are you sure {size} is a valid size?', file=sys.stderr)
			sys.exit(1)
		solvable_input = input(f'Dear {os.environ["USER"]}, should the puzzle be solvable? (Y/N) ').lower()
		solvable = (len(solvable_input) > 0 and solvable_input[0] == 'y')
		print(f'Noted. Puzzle will{" not" if solvable == False else ""} be solvable.')
		iterations = input(f'Dear {os.environ["USER"]}, how many times should we shuffle the puzzle? (default=1000) ')
		try:
			if not iterations: iterations = 0
			iterations = int(iterations)
		except ValueError:
			print(f'Error. "{iterations}" is not a valid number.', file=sys.stderr)
			sys.exit(1)
		self.size = size
		puzz = make_puzzle(size, solvable, iterations)
		self.original_position = np.array(puzz, dtype=np.uint16).reshape((self.size, self.size))
		self.set_goals()
		print(self.original_position)
		accepted_answer = 'newoneplease'
		a = input(f'Dear {os.environ["USER"]}, this is the generated puzzle.\nType "{accepted_answer}" to generate a new one. ')
		if a == accepted_answer:
			self.create_random_state()

	@staticmethod
	def get_direction(key: int) -> Direction:
		match key:
			case 72:  # ARROW_UP
				return Direction.UP
			case 75:  # ARROW_LEFT
				return Direction.LEFT
			case 77:  # ARROW_RIGHT
				return Direction.RIGHT
			case 80:  # ARROW_DOWN
				return Direction.DOWN
		raise KeyError

	def play_interactive(self) -> int:
		gamestate = self.create_starting_state()
		while not np.array_equal(gamestate.rows, self.goal_matrix):
			print(gamestate.rows)
			direction, key = '', get_keypress()
			try:
				direction = self.get_direction(key)
				if not gamestate.is_possible(direction):
					raise IndexError
				gamestate.do_move(direction)
			except IndexError:
				print(f'{direction} is not a legal move')
		return 0
