import numpy as np
from srcs.gamestate import Gamestate


def misplaced_tiles(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	val = 0
	for (idx, cur), (idx2, goal) in zip(np.ndenumerate(current_matrix), np.ndenumerate(goal_matrix)):
		if cur == goal:
			val += 1
	return val


# Not a typo, Mannhattan is a real place in TF2
def mannhattan_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	val = 0
	for y, _ in enumerate(current_matrix):
		for x, _ in enumerate(current_matrix[y]):
			item = current_matrix[y][x]
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val += abs(y - goal_pos[0][0]) + abs(x - goal_pos[1][0])
	return val


def set_heuristic_values(state: Gamestate, goal_matrix: np.ndarray) -> None:
	state.mannhattan = mannhattan_distance(state.rows, goal_matrix)
	state.misplaced = mannhattan_distance(state.rows, goal_matrix)
	state.linear = 0
	state.total = state.mannhattan + state.misplaced
