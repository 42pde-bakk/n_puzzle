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


def euclidean_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> float:
	val = 0
	for y, _ in enumerate(current_matrix):
		for x, item in enumerate(current_matrix[y]):
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val += (abs(y - goal_pos[0][0]) + abs(x - goal_pos[1][0])) ** 2
	return np.sqrt(val)


def minkowski_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray, p: int) -> float:
	val = 0
	for y, _ in enumerate(current_matrix):
		for x, item in enumerate(current_matrix[y]):
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val += (y - goal_pos[0][0]) ** p + (x - goal_pos[1][0]) ** p
	return val ** (1 / p)


def set_heuristic_values(state: Gamestate, goal_matrix: np.ndarray, args) -> None:
	"""Set various heuristic values in the provided Gamestate class"""
	# TODO Add arguments parsing
	if not args.uniform:
		total_h = 0
		if args.manhattan:
			total_h += mannhattan_distance(state.rows, goal_matrix)
		if args.misplaced:
			total_h += misplaced_tiles(state.rows, goal_matrix)
		if args.euclidean:
			total_h += euclidean_distance(state.rows, goal_matrix)
		if args.minkowski:
			total_h += minkowski_distance(state.rows, goal_matrix, p=2)
		state.h_total = total_h
