import enum
from typing import Tuple
import numpy as np


class Direction(enum.IntEnum):
	"""IntEnum to represent a move direction"""
	DOWN = 0  # 0-pos changes with same pos in row below (zero-pos
	LEFT = 1  # 0-pos changes with pos-1
	UP = 2  # 0-pos changes with same pos in row above (zero-pos - size)
	RIGHT = 3  # 0-pos swaps with pos+1 (zero-pos + 1)

	def __str__(self) -> str:
		return self.name

	def __int__(self):
		return self.value


def get_movepos(zero_pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
	"""Returns the position the empty tile would move to"""
	x, y = zero_pos

	if direction in (Direction.UP, Direction.DOWN):
		y = (y - 1) if direction == Direction.UP else (y + 1)
	elif direction in (Direction.LEFT, Direction.RIGHT):
		x = (x - 1) if direction == Direction.LEFT else (x + 1)
	return x, y


class Gamestate:
	"""Class to contain information about the current state of the puzzle"""
	size = 0

	def __init__(self) -> None:
		self.zero_pos = (0, 0)
		self.rows = np.ndarray
		self.parent = None
		self.mannhattan = self.misplaced = self.linear = self.total = 0
		self.moves = 0

	def give_copy(self, x):
		"""Method to copy over values because deepcopying can be slow"""
		self.moves = x.moves
		self.zero_pos = x.zero_pos
		self.rows = x.rows
		self.parent = x

	def get_heuristics(self) -> str:
		"""Return string with this gamestate's moves and heuristic values"""
		return f'moves: {self.moves}\n' \
			f'mannhattan distance: {self.mannhattan}\n' \
			f'misplaced tiles: {self.misplaced}\n' \
			f'total H: {self.total}'

	def __eq__(self, other):
		return np.array_equal(self.rows, other.rows)

	def __lt__(self, other):
		return self.moves < other.moves

	def find_zero_pos(self) -> Tuple[int, int]:
		"""Returns the position of the empty tile inside the matrix"""
		position_arr = np.where(self.rows == 0)
		if position_arr[0].size == 0:
			raise IndexError
		return position_arr[1][0], position_arr[0][0]  # x, y

	def is_possible(self, direction: Direction) -> bool:
		"""Returns whether the move in this direction is possible"""
		if direction == Direction.UP:
			assert self.zero_pos[1] != 0
		elif direction == Direction.DOWN:
			assert self.zero_pos[1] < Gamestate.size - 1
		elif direction == Direction.LEFT:
			assert self.zero_pos[0] > 0
		else:
			assert self.zero_pos[0] < Gamestate.size - 1
		return True

	def do_move(self, direction: Direction):
		"""Execute move in new the new gamestate and increment the move amount"""
		move_pos = get_movepos(zero_pos=self.zero_pos, direction=direction)
		self.rows[self.zero_pos[1]][self.zero_pos[0]], self.rows[move_pos[1]][move_pos[0]] = \
			self.rows[move_pos[1]][move_pos[0]], self.rows[self.zero_pos[1]][self.zero_pos[0]]
		self.zero_pos = move_pos
		self.moves += 1
		return self

	def __str__(self):
		string = f'{self.rows}\n'
		return string
