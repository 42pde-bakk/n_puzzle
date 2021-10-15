import numpy as np
from srcs.npuzzle import Npuzzle


def calc_dist(enumeration_tuple) -> int:
	y_pos, x_pos = enumeration_tuple[0]
	ideal_pos = enumeration_tuple[1] - 1
	if ideal_pos == 0:
		return 0
	x_goal, y_goal = ideal_pos % 3, ideal_pos // 3
	return abs(x_pos - x_goal) + abs(y_pos - y_goal)


def manhattan_distance(gamestate: Npuzzle):
	return sum(map(calc_dist, np.ndenumerate(gamestate.rows)))
