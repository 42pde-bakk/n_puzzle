import numpy as np


def clean_row(row: str) -> list[str]:
	return row.split(sep='#', maxsplit=1)[0].split()  # Discard everything after the first '#' and remove whitespaces


def parse_header(row: str) -> int:
	cleaned_row = clean_row(row)
	return int(cleaned_row[0])


def parserow(row: str) -> list[int]:
	cleaned_row = clean_row(row)
	assert row
	return [int(item) for item in cleaned_row]


def assert_validity(size: int, rows: np.ndarray) -> None:
	assert size == rows.shape[0] == rows.shape[1]
	assert size * size == len(set(rows.flatten()))
