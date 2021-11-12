import numpy as np
from srcs.gamestate import Gamestate


def misplaced_tiles(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Iterate through the matrix and sum the amount of tiles not in their goal position"""
	return sum(current_matrix != goal_matrix)


def optimized_misplaced_tiles(state: Gamestate, goal_matrix: np.ndarray) -> int:
	"""Take the misplaced tiles heuristic of the parent and edit it for the newly moved tile"""
	state.h_misplaced = state.parent.h_misplaced
	p0 = state.parent.zero_pos  # x, y
	c0 = state.zero_pos  # x, y

	if state.parent.rows[c0[1]][c0[0]] == goal_matrix[c0[1]][c0[0]]:
		# Remove 1 score if the moved tile used to be in the right position
		# Take the parent state and use the current state's zero_pos
		# And check if it used to be in the current position
		state.h_misplaced -= 1
	elif state.rows[p0[1]][p0[0]] == goal_matrix[p0[1]][p0[0]]:
		# Add 1 score if it now is in the correct position
		state.h_misplaced += 1
	return state.h_misplaced


# Not a typo, Mannhattan is a real place in TF2
def mannhattan_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Iterate through the matrix and sum the manhattan distances"""
	val = 0
	for y, row in enumerate(current_matrix):
		for x, item in enumerate(row):
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val += abs(y - goal_pos[0][0]) + abs(x - goal_pos[1][0])
	return val


# Not a typo, Mannhattan is a real place in TF2
def optimized_mannhattan_distance(state: Gamestate, goal_matrix: np.ndarray) -> int:
	"""Take the manhattan distance of the parent gamestate and edit the distance of the newly moved tile"""
	state.h_manhattan = state.parent.h_manhattan
	p0 = state.parent.zero_pos  # x, y
	c0 = state.zero_pos  # x, y
	tile = state.parent.rows[c0[1]][c0[0]]
	goal_pos = np.where(goal_matrix == tile)
	newdist = abs(p0[1] - goal_pos[0][0]) + abs(p0[0] - goal_pos[1][0])
	prevdist = abs(c0[1] - goal_pos[0][0]) + abs(c0[0] - goal_pos[1][0])
	state.h_manhattan -= prevdist
	state.h_manhattan += newdist
	return state.h_manhattan


def weighted_manhattan_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Similar to manhattan distance but give extra priority to edge pieces and even more to corner pieces"""
	val = 0
	for y, row in enumerate(current_matrix):
		for x, item in enumerate(row):
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val2 = abs(y - goal_pos[0][0]) + abs(x - goal_pos[1][0])
				if goal_pos[0][0] == 0 or goal_pos[0][0] == current_matrix.shape[0]:
					val2 *= 2
				if goal_pos[1][0] == 0 or goal_pos[1][0] == current_matrix.shape[0]:
					val2 *= 2
				val += val2
	return val


# noinspection PyTypeChecker
def correctlines(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	val = 0
	n, _ = current_matrix.shape
	for i in range(n):
		if sum(current_matrix[i, :] == goal_matrix[i, :]) == n:
			val += 1
		if sum(current_matrix[:, i] == goal_matrix[:, i]) == n:
			val += 1
	return val


# noinspection PyTypeChecker
def optimized_correctlines(state: Gamestate, goal_matrix: np.ndarray) -> int:
	n = Gamestate.size
	state.h_correctlines = state.parent.h_correctlines
	current_emptytile_pos = state.zero_pos
	parent_emptytile_pos = state.parent.zero_pos

	if sum(state.parent.rows[parent_emptytile_pos[0], :] == goal_matrix[parent_emptytile_pos[0], :]) == n:
		state.h_correctlines -= 1  # Check the parent's row that contained the empty tile
	if sum(state.parent.rows[:, parent_emptytile_pos[1]] == goal_matrix[:, parent_emptytile_pos[1]]) == n:
		state.h_correctlines -= 1  # Check the parent's column that contained the empty tile
	if sum(state.parent.rows[current_emptytile_pos[0], :] == goal_matrix[current_emptytile_pos[0], :]) == n:
		state.h_correctlines -= 1  # Check the parent's row that contains the empty tile in the current state
	if sum(state.parent.rows[:, current_emptytile_pos[1]] == goal_matrix[:, current_emptytile_pos[1]]) == n:
		state.h_correctlines -= 1  # Check the parent's column that contains the empty tile in the current state
	if sum(state.rows[parent_emptytile_pos[0], :] == goal_matrix[parent_emptytile_pos[0], :]) == n:
		state.h_correctlines += 1  # Check the parent's row that contained the empty tile
	if sum(state.rows[:, parent_emptytile_pos[1]] == goal_matrix[:, parent_emptytile_pos[1]]) == n:
		state.h_correctlines += 1  # Check the parent's column that contained the empty tile
	if sum(state.rows[current_emptytile_pos[0], :] == goal_matrix[current_emptytile_pos[0], :]) == n:
		state.h_correctlines += 1  # Check the parent's row that contains the empty tile in the current state
	if sum(state.rows[:, current_emptytile_pos[1]] == goal_matrix[:, current_emptytile_pos[1]]) == n:
		state.h_correctlines += 1  # Check the parent's column that contains the empty tile in the current state
	return state.h_correctlines


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
				val1 = abs(y - goal_pos[0][0]) ** p + abs(x - goal_pos[1][0]) ** p
				val += val1
	return val ** (1 / p)


def set_heuristic_values(state: Gamestate, goal_matrix: np.ndarray, args) -> None:
	"""Set various heuristic values in the provided Gamestate class"""
	if not args.uniform:
		total_h = 0
		if args.manhattan:
			state.h_manhattan = mannhattan_distance(state.rows, goal_matrix)
			total_h += state.h_manhattan
		if args.weightedmanhattan:
			total_h += weighted_manhattan_distance(state.rows, goal_matrix)
		if args.misplaced:
			total_h += misplaced_tiles(state.rows, goal_matrix)
		if args.euclidean:
			total_h += euclidean_distance(state.rows, goal_matrix)
		if args.minkowski:
			total_h += minkowski_distance(state.rows, goal_matrix, p=2)
		if args.correctlines:
			total_h += correctlines(state.rows, goal_matrix)
		state.h_total = total_h


def set_heuristic_values_timeoptimized(state: Gamestate, goal_matrix: np.ndarray, args) -> None:
	"""Set various heuristic values in the provided Gamestate class using it's parents heuristic values"""
	if not args.uniform:
		state.h_total = 0
		if args.manhattan:
			state.h_total += optimized_mannhattan_distance(state, goal_matrix)
		if args.weightedmanhattan:
			state.h_total += weighted_manhattan_distance(state.rows, goal_matrix)
		if args.misplaced:
			state.h_misplaced += optimized_misplaced_tiles(state, goal_matrix)
		if args.euclidean:
			state.h_total += euclidean_distance(state.rows, goal_matrix)
		if args.minkowski:
			state.h_total += minkowski_distance(state.rows, goal_matrix, p=2)
		if args.correctlines:
			state.h_total += optimized_correctlines(state, goal_matrix)
