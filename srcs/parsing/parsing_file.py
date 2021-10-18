import numpy as np
from typing import List, Tuple


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
