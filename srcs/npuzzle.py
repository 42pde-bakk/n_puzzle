import sys
import enum
import numpy as np
from srcs.parsing.parsing_file import parse_header, parserow, assert_validity


class Direction(enum.IntEnum):
	UP = 0  # 0-pos changes with same pos in row above (zero-pos - size)
	RIGHT = 1  # 0-pos swaps with pos+1 (zero-pos + 1)
	DOWN = 2  # 0-pos changes with same pos in row below (zero-pos
	LEFT = 3  # 0-pos changes with pos-1


def get_movepos(zero_pos: tuple[int, int], direction: Direction) -> tuple[int, int]:
	x, y = zero_pos

	if direction in (Direction.UP, Direction.DOWN):
		y = (y - 1) if direction == Direction.UP else (y + 1)
	elif direction in (Direction.LEFT, Direction.RIGHT):
		x = (x - 1) if direction == Direction.LEFT else (x + 1)
	return x, y


def is_sorted(arr: np.ndarray) -> bool:
	return np.all(arr[:-1] <= arr[1:])


class Npuzzle:
	"""Class to contain information about the current state of the puzzle"""
	def __init__(self) -> None:
		self.size = 0
		self.moves = 0
		self.zero_pos = (0, 0)
		self.rows = np.ndarray

	def give_copy(self, x):
		self.size = x.size
		self.moves = x.moves
		self.zero_pos = x.zero_pos
		self.rows = x.rows

	def parse_puzzle(self, rows: list[str]):
		self.size = 0
		self.rows = self.readrows(rows)
		self.zero_pos = self.find_zero_pos()  # Tuple[xcoord, ycoord]
		print(f'og is:\n{self.rows}')
		assert_validity(self.size, self.rows)

	def set_size(self, size: int):
		self.size = size

	def find_zero_pos(self) -> tuple[int, int]:
		for y, row in enumerate(self.rows):
			for x, item in enumerate(row):
				if item == 0:
					print(f'zero_pos = ({x}, {y})')
					return x, y
		raise IndexError

	def addrow(self, row: str) -> list:
		if self.size == 0:
			try:
				self.set_size(parse_header(row))
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

	def readrows(self, rows: list[str]) -> np.ndarray:
		return np.array([temp for row in rows if (temp := self.addrow(row))])

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
		flattened_puzzle = self.rows.flatten()
		return flattened_puzzle[-1] == 0 and is_sorted(flattened_puzzle[:-1])

	def do_move(self, direction: Direction, old_gamestates: set):
		move_pos = get_movepos(zero_pos=self.zero_pos, direction=direction)
		self.rows[self.zero_pos[1]][self.zero_pos[0]], self.rows[move_pos[1]][move_pos[0]] = \
			self.rows[move_pos[1]][move_pos[0]], self.rows[self.zero_pos[1]][self.zero_pos[0]]
		self.zero_pos = move_pos
		self.moves += 1

		value = np.array2string(self.rows.flatten())
		if value in old_gamestates:
			raise KeyError
		old_gamestates.add(value)
		return self

	def __str__(self):
		string = f'{self.rows}\n'
		if self.is_solved():
			string += 'Solved '
		else:
			string += 'Unsolved '
		return string + f'in {self.moves} steps.'
