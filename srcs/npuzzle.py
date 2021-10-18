import sys
import enum
import numpy as np
from typing import Tuple, List

from srcs.parsing.parsing_file import parse_header, parserow


class Direction(enum.IntEnum):
	UP = 0  # 0-pos changes with same pos in row above (zero-pos - size)
	RIGHT = 1  # 0-pos swaps with pos+1 (zero-pos + 1)
	DOWN = 2  # 0-pos changes with same pos in row below (zero-pos
	LEFT = 3  # 0-pos changes with pos-1

	def __str__(self) -> str:
		return self.name


def get_movepos(zero_pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
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
		self.moves = 7
		self.zero_pos = (0, 0)
		self.rows = np.ndarray

	def give_copy(self, x):
		self.size = x.size
		self.moves = x.moves
		self.zero_pos = x.zero_pos
		self.rows = x.rows

	def parse_puzzle(self, rows: List[str]):
		self.size = 0
		self.rows = self.readrows(rows)
		self.zero_pos = self.find_zero_pos()  # Tuple[xcoord, ycoord]
		print(f'og is:\n{self.rows}\n\n')

	def __lt__(self, other):
		return self.moves < self.moves

	def set_size(self, size: int):
		self.size = size

	def find_zero_pos(self) -> Tuple[int, int]:
		for y, row in enumerate(self.rows):
			for x, item in enumerate(row):
				if item == 0:
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

	def readrows(self, rows: List[str]) -> np.ndarray:
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

	def add_move(self, direction: Direction) -> None:
		self.moves *= 10
		self.moves += int(direction)

	def do_move(self, direction: Direction, old_gamestates: set):
		move_pos = get_movepos(zero_pos=self.zero_pos, direction=direction)
		self.rows[self.zero_pos[1]][self.zero_pos[0]], self.rows[move_pos[1]][move_pos[0]] = \
			self.rows[move_pos[1]][move_pos[0]], self.rows[self.zero_pos[1]][self.zero_pos[0]]
		self.zero_pos = move_pos
		self.add_move(direction)

		value = int(''.join(map(str, self.rows.flatten())))
		if value in old_gamestates:
			raise KeyError
		old_gamestates.add(value)
		return self

	def extract_move_sequence(self) -> List[str]:
		move_sequence = str(self.moves).replace('7', '')
		return [str(Direction(int(move))) for move in move_sequence]

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
