import numpy as np
from typing import List, Tuple


def is_even(nb: int) -> bool:
	return nb % 2 == 0


def is_odd(nb: int) -> bool:
	return not is_even(nb)


def clean_row(row: str) -> List[str]:
	"""Remove whitespaces, discard everything after the first '#' and return the row as a list"""
	return row.split(sep='#', maxsplit=1)[0].split()


def parse_header(row: str) -> int:
	"""Clean row and try to return the first value as an int"""
	cleaned_row = clean_row(row)
	return int(cleaned_row[0])


def parserow(row: str) -> List[int]:
	"""Make sure the row is valid"""
	cleaned_row = clean_row(row)
	assert row
	return [int(item) for item in cleaned_row]


def assert_validity(size: int, rows: np.ndarray) -> None:
	"""Assert all rows are equal in length and without duplicate items"""
	assert size == rows.shape[0] == rows.shape[1]
	puzzle_as_set = set(rows.flatten())
	assert len(puzzle_as_set) == size * size
	assert all(x in range(0, size * size) for x in puzzle_as_set)
