import numpy as np
from srcs.gamestate import Gamestate


def misplaced_tiles(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Iterate through the matrix and sum the amount of tiles not in their goal position"""
	val = 0
	for (_, cur), (_, goal) in zip(np.ndenumerate(current_matrix), np.ndenumerate(goal_matrix)):
		if cur != goal:
			val += 1
	return val


# Not a typo, Mannhattan is a real place in TF2
def mannhattan_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Iterate through the matrix and sum the manhattan distances"""
	val = 0
	for y, _ in enumerate(current_matrix):
		for x, _ in enumerate(current_matrix[y]):
			item = current_matrix[y][x]
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val += abs(y - goal_pos[0][0]) + abs(x - goal_pos[1][0])
	return val


def set_heuristic_values(state: Gamestate, goal_matrix: np.ndarray, args) -> None:
	"""Set various heuristic values in the provided Gamestate class"""
	# TODO Add arguments parsing
	if not args.uniform:
		total_h = 0
		if args.manhattan:
			total_h += mannhattan_distance(state.rows, goal_matrix)
		if args.misplaced:
			total_h += misplaced_tiles(state.rows, goal_matrix)
		state.h_total = total_h
