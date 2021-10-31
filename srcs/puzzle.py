import sys
import copy
from typing import List, Tuple
import numpy as np
from srcs.parsing.parsing_file import parse_header, parserow
from srcs.gamestate import Gamestate


# Create a spiral matrix from a given list
def to_spiralarray(arr: np.ndarray) -> np.ndarray:
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
	def __init__(self):
		self.size = 0
		self.goal_matrix = np.ndarray
		self.original_position = np.ndarray

	# noinspection PyTypeChecker
	def set_goals(self):
		self.goal_matrix = to_spiralarray(np.array([x for x in range(1, self.size ** 2)] + [0], dtype=np.uint16).reshape((self.size, self.size)))
		print(f'goal_matrix is {self.goal_matrix}')

	def create_starting_state(self) -> Gamestate:
		gamestate = Gamestate()
		gamestate.rows = copy.deepcopy(self.original_position)
		Gamestate.size = self.size
		gamestate.zero_pos = gamestate.find_zero_pos()
		print(f'gamestate.parent={gamestate.parent}')
		return gamestate

	def addrow(self, row: str) -> list:
		if self.size == 0:
			try:
				self.size = parse_header(row)
			except IndexError:
				return []
		else:
			try:
				parsed_row = parserow(row)
				return parsed_row
			except (AssertionError, ValueError) as e:
				print(f'row {row} is invalid.', file=sys.stderr)
				raise e
		return []

	def readrows(self, rows: List[str]) -> np.ndarray:
		return np.array([temp for row in rows if (temp := np.array(self.addrow(row), dtype=np.uint16)).size])

	def parse_puzzle(self, rows: List[str]):
		self.size = 0
		self.original_position = self.readrows(rows)
		print(type(self.original_position), type(self.original_position[0]), self.original_position[0].dtype)
		# self.zero_pos = self.find_zero_pos()  # Tuple[xcoord, ycoord]
		print(f'og is:\n{self.original_position}\n\n')
		self.set_goals()

	# noinspection PyTypeChecker
	def find_zero_pos(self) -> Tuple[int, int]:
		for y, row in enumerate(self.original_position):
			for x, item in enumerate(row):
				if item == 0:
					return x, y
		raise IndexError
