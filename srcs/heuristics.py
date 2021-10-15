import numpy as np
from srcs.npuzzle import Npuzzle

g_puzzle_size = 0


def calc_manhattan_dist(enumeration_tuple) -> int:
	y_pos, x_pos = enumeration_tuple[0]
	ideal_pos = enumeration_tuple[1] - 1
	if enumeration_tuple[1] == 0:
		return 0
	x_goal, y_goal = ideal_pos % g_puzzle_size, ideal_pos // g_puzzle_size
	return abs(x_pos - x_goal) + abs(y_pos - y_goal)


def calc_minkowski_distance(enumeration_tuple, p) -> int:
	y_pos, x_pos = enumeration_tuple[0]
	ideal_pos = enumeration_tuple[1] - 1
	if enumeration_tuple[1] == 0:
		return 0
	x_goal, y_goal = ideal_pos % 3, ideal_pos // 3
	return abs(x_pos - x_goal) + abs(y_pos - y_goal) ** p


def manhattan_distance(gamestate: Npuzzle) -> int:
	global g_puzzle_size
	g_puzzle_size = gamestate.size
	return sum(map(calc_manhattan_dist, np.ndenumerate(gamestate.rows)))


def minkowski_distance(gamestate: Npuzzle, p) -> int:
	global g_puzzle_size
	g_puzzle_size = gamestate.size
	return sum(map(calc_minkowski_distance, np.ndenumerate(gamestate.rows))) ** (1 / p)
