import enum
import numpy as np
from typing import Tuple, List


class Direction(enum.IntEnum):
	DOWN = 0  # 0-pos changes with same pos in row below (zero-pos
	LEFT = 1  # 0-pos changes with pos-1
	UP = 2  # 0-pos changes with same pos in row above (zero-pos - size)
	RIGHT = 3  # 0-pos swaps with pos+1 (zero-pos + 1)

	def __str__(self) -> str:
		return self.name

	def __int__(self):
		return self.value


def get_movepos(zero_pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
	x, y = zero_pos

	if direction in (Direction.UP, Direction.DOWN):
		y = (y - 1) if direction == Direction.UP else (y + 1)
	elif direction in (Direction.LEFT, Direction.RIGHT):
		x = (x - 1) if direction == Direction.LEFT else (x + 1)
	return x, y


class Npuzzle:
	"""Class to contain information about the current state of the puzzle"""
	def __init__(self) -> None:
		self.size = 0
		self.moves = 7
		self.zero_pos = (0, 0)
		self.rows = np.ndarray
		self.parent = None

	def give_copy(self, x):
		self.size = x.size
		self.moves = x.moves
		self.zero_pos = x.zero_pos
		self.rows = x.original_position
		self.parent = x

	def __eq__(self, other):
		return np.array_equal(self.rows, other.original_position)

	def __lt__(self, other):
		return self.move_amount() < other.move_amount()

	def set_size(self, size: int):
		self.size = size

	def find_zero_pos(self) -> Tuple[int, int]:
		for y, row in enumerate(self.rows):
			for x, item in enumerate(row):
				if item == 0:
					return x, y
		raise IndexError

	def is_possible(self, direction: Direction) -> bool:
		if direction == Direction.UP:
			assert self.zero_pos[1] != 0
		elif direction == Direction.DOWN:
			assert self.zero_pos[1] < self.size - 1
		elif direction == Direction.LEFT:
			assert self.zero_pos[0] > 0
		else:
			assert self.zero_pos[0] < self.size - 1
		return True

	def is_solved(self) -> bool:
		spiral_arr = spiral_traversal(self.rows)
		return np.all(spiral_arr[:-1] <= spiral_arr[1:]) and spiral_arr[-1] == 0

	def add_move(self, direction: Direction) -> None:
		self.moves *= 10
		self.moves += int(direction)

	def do_move(self, direction: Direction):
		move_pos = get_movepos(zero_pos=self.zero_pos, direction=direction)
		self.rows[self.zero_pos[1]][self.zero_pos[0]], self.rows[move_pos[1]][move_pos[0]] = \
			self.rows[move_pos[1]][move_pos[0]], self.rows[self.zero_pos[1]][self.zero_pos[0]]
		self.zero_pos = move_pos
		self.add_move(direction)
		return self

	def extract_move_sequence(self) -> List[str]:
		move_sequence = str(self.moves).replace('7', '')
		return [str(Direction(int(move))) for move in move_sequence]

	def extract_move_sequence_as_enums(self) -> List[Direction]:
		move_sequence = str(self.moves).replace('7', '')
		return [Direction(int(move)) for move in move_sequence]

	def move_amount(self) -> int:
		return len(str(self.moves)) - 1

	def __str__(self):
		string = f'{self.rows}\n'
		if self.is_solved():
			string += 'Solved '
		else:
			string += 'Unsolved '
		string += f'in {len(str(self.moves)) - 1} steps.\n'
		string += f'Move sequence is {str(self.extract_move_sequence())}.\n'
		return string
