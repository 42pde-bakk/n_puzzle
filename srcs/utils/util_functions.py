import numpy as np
from typing import Tuple


def is_even(nb: int) -> bool:
	"""Really?"""
	return nb % 2 == 0


def is_odd(nb: int) -> bool:
	"""Really?"""
	return not is_even(nb)


def find_pos_in_array(state: np.ndarray, value: int = 0) -> Tuple[int, int]:
	arr = np.where(state == value)
	return arr[0][0], arr[1][0]
