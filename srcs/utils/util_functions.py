from typing import Tuple
import numpy as np
from msvcrt import getch


def is_even(nb: int) -> bool:
	"""Really?"""
	return nb % 2 == 0


def is_odd(nb: int) -> bool:
	"""Really?"""
	return not is_even(nb)


def find_pos_in_array(state: np.ndarray, value: int = 0) -> Tuple[int, int]:
	"""Return the x, y position of the given value in the ndarray"""
	arr = np.where(state == value)
	return arr[0][0], arr[1][0]


def get_keypress():
	key = ord(getch())
	if key in [3, 4, 27, 28]:  # 3=Ctrl+C, 4=CTRL+D, 28=CTRL+\, 27=ESC
		raise KeyboardInterrupt
	# elif key == 13:  # Enter
	# 	select()
	if key == 224:  # Special keys (arrows, f keys, ins, del, etc...)
		key = ord(getch())
		return key
	return get_keypress()
