import numpy as np
import sys
from srcs.parsing.parsing_file import parse_header, parserow, assert_validity


class Npuzzle:
	def __init__(self, rows: list[str]) -> None:
		self.size = 0
		self.rows = self.readrows(rows)
		assert_validity(self.size, self.rows)

	def set_size(self, size: int):
		self.size = size

	def addrow(self, row: str) -> list:
		if self.size == 0:
			try:
				self.set_size(parse_header(row))
			except IndexError:
				return list()
		else:
			try:
				parsed_row = parserow(row)
				return parsed_row
			except (AssertionError, ValueError) as e:
				print(f'row {row} is invalid.', file=sys.stderr)
				raise e

	def readrows(self, rows: list[str]) -> np.ndarray:
		return np.array([temp for row in rows if (temp := self.addrow(row))])
