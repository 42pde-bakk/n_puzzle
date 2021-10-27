import numpy as np


def misplaced_tiles(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	val = 0
	for (idx, cur), (idx2, goal) in zip(np.ndenumerate(current_matrix), np.ndenumerate(goal_matrix)):
		print(f'cur={idx, cur}, goal={idx2, goal}')
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
